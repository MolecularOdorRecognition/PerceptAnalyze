import urllib.request
import gzip
import csv
import json
from bson.objectid import ObjectId
import os
import logging

logging.basicConfig(filename="log.out", filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    file = open('word.csv', 'r', encoding="utf8")  # Open file
    read = csv.reader(file, delimiter=',')
except OSError as err:
    logger.error("OS error: {0}".format(err))
except IOError as io:
    logger.error("IO Erroe", io)

f = open('newjson.txt', 'w')  # psuedo code to create file
f.close()

xp = []  # list of words to download
yp = []  # list of normal words
zp = []  # list of stem words

# Creating 2 lists
for row in read:
    # print(row)
    row[0] = row[0].strip()
    # print(row)
    if row[0][-1] == '*':
        zp.extend(row)          # Separating * words
    else:
        yp.extend(row)

# Creating a list to download
for z in yp:
    z = z.strip()
    if z[:2] not in xp:
        xp.append(z[:2])

xp.sort()
# xp = ['ta']
print(xp)


# Class Encoder to dump dictionary in json
class Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            else:
                return obj


# search function for matching stem words
def searchf(y, zp):
    for x in zp:
        if y[:len(x)-1] == x[:-1]:
            return True
    return False


for i in range(len(xp)):
    target = open('newjson.txt', 'r')
    logger.info('downloading '+xp[i])
    try:
        urllib.request.urlretrieve("http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"+xp[i]+".gz", xp[i]+".gz")
    except:
        logger.error("Error Downloading "+xp[i])
        continue
    search = {}
    # Reading search from newjson.txt
    tar = target.read()
    if len(tar) > 0:
        search = json.loads(tar)
    target.close()

    for row in yp:
        if row not in search.keys():
                search[row] = {}
    for row in zp:
        if row[:-1] not in search.keys():
                search[row[:-1]] = {}

    logger.info('Opening '+xp[i])
    # Opening .gz file and searching for words in yp or zp
    with gzip.open(xp[i]+'.gz', 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            x = str(row[0])
            y, z = x.split(' ')
            if y.lower() in yp:
                    if z.lower() in yp or searchf(z.lower(), zp):
                        if z.lower() not in search[y.lower()].keys():
                            search[y.lower()][z.lower()] = 1
                        else:
                            search[y.lower()][z.lower()] += 1
            else:
                if searchf(y.lower(), zp):
                    if y.lower() not in search.keys():
                            # print(type(y), type(search))
                            '''if '_' in y.lower():
                                d, e = y.split("_")
                                y = d.lower()'''
                            search[y.lower()] = {}
                            logger.info('new key '+y.lower())
                            yp.append(y.lower())
                            if z.lower() in yp or searchf(z.lower(), zp):
                                search[y.lower()][z.lower()] = 1

    target = open('newjson.txt', 'w')
    jso = json.dumps(search, cls=Encoder)  # dumping search
    target.truncate()
    target.write(jso)  # writing search
    target.close()
    f.close()
    logger.info('Removing '+xp[i])
    os.remove(xp[i]+".gz")

file.close()
