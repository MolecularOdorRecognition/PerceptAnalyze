import urllib.request
import gzip
import csv
import json
from bson.objectid import ObjectId
import os
import logging

logging.basicConfig(filename="sample.log", filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    file = open('flavornetPercepts.csv', 'r', encoding="utf8")
    nfile = open('superscentPercepts.csv', 'r', encoding="utf8")  # Opening the csv files to read words required
    read = csv.reader(file, delimiter=',')    # assigning a csv reader to it
    reading = csv.reader(nfile, delimiter=',')
except OSError as err:
    logger.error("OS error: {0}".format(err))
except IOError as io:
    logger.error("IO Erroe", io)


try:
    target2 = open('json.txt', 'w')
    target = open('newjson.txt', 'w')  # creating files to write
except OSError as err:
    logger.error("OS error: {0}".format(err))
except IOError as io:
    logger.error("IO Erroe", io)
finally:
    target.close()
    target2.close()

xp = []
yp = []  # Defining lists to store downloading words,normal words respectively
zp = []

for row in read:
    yp.extend(row)
for row in reading:
    zp.extend(row)

# Adding words to download in xp
for z in yp:
    z = z.strip()
    if z[:2] not in xp:
        xp.append(z[:2])
for q in zp:
    q = q.strip()
    if q[:2] not in xp:
        xp.append(q[:2])

xp.sort()   # sorting xp
# yp.sort()
# print(zp)
# print(len(xp))
# xp = ['-e', ' e', 'oi']


# Class Encoder to dump dictionary in json
class Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            else:
                return obj

# For all words in xp
for i in range(len(xp)):
    target2 = open('json.txt', 'r')
    target = open('newjson.txt', 'r')
    logger.info('downloading '+xp[i]) # downloading from googlebooks dataset
    try:
        urllib.request.urlretrieve("http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"+xp[i]+".gz", xp[i]+".gz")
    except:
        logger.error("Error Downloading "+xp[i])
        continue
    search = {}
    search2 = {}
    tar2 = target2.read()  # reading the previous data stored in files if any
    tar = target.read()
    if len(tar) > 0:
        search = json.loads(tar)
    if len(tar2) > 0:
        search2 = json.loads(tar2)
    target2.close()
    target.close()  # closing the files

    # adding keys to search and search2
    for row in yp:
        if row not in search.keys():
                search[row] = {}

    for row in zp:
        if row not in search2.keys():
                search2[row] = {}

    logger.info('Opening '+xp[i])
    try:
        # opening the .gzip downloaded file
        with gzip.open(xp[i]+'.gz', 'rt', encoding='utf-8') as f:
            # file_content = f.read()
            reader = csv.reader(f, delimiter='\t') # reading as tab separted values
            for row in reader:
                x = str(row[0])
                y, z = x.split(' ')
                # checking if y,z exist in our word list yp
                if y.lower() in yp:
                    if z.lower() in yp:
                        if z.lower() not in search[y.lower()].keys():
                            search[y.lower()][z.lower()] = 1
                        else:
                            search[y.lower()][z.lower()] += 1
                if y.lower() in zp:
                    if z.lower() in zp:
                        if z.lower() not in search2[y.lower()].keys():
                            search2[y.lower()][z.lower()] = 1
                        else:
                            search2[y.lower()][z.lower()] += 1
    except OSError as err:
        logger.error("OS error: {0}".format(err))
    except IOError as io:
        logger.error("IO Erroe", io)

    target2 = open('json.txt', 'w')
    target = open('newjson.txt', 'w')
    jso = json.dumps(search, cls=Encoder)  # dumping dict into json
    jsooo = json.dumps(search2, cls=Encoder)
    target2.truncate()
    target.truncate()
    target2.write(jsooo) # writing in the file
    target.write(jso)
    target.close()
    target2.close()
    f.close()
    logger.info('Removing '+xp[i])
    # print('Removing '+xp[i])
    os.remove(xp[i]+".gz")  # Removing the downloaded file

file.close()
nfile.close()
