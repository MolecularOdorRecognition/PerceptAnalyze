import networkx as nx
import json
import csv

target = open('newjson.txt', 'r')  # Open files for reading
target2 = open('json.txt', 'r')
tar = target.read()
tar2 = target2.read()
search = json.loads(tar)
search2 = json.loads(tar2)  # Loading json format to dict search

g2 = nx.Graph()
g = nx.Graph()    # Creating graphs

# Adding EDGES to graphs g and g2 with thier respective weights
for x in search.keys():
    # if len(dict(search[x]).keys()) >= 0:
    if type(search[x]) == dict:
        for y in search[x].keys():
            # z = {search[x][y]}
            g.add_edge(x, y, weight=search[x][y])
            # print(x, y, g.get_edge_data(x, y))

for x in search2.keys():
    # if len(dict(search[x]).keys()) >= 0:
    if type(search2[x]) == dict:
        for y in search2[x].keys():
            # z = {search[x][y]}
            g2.add_edge(x, y, weight=search2[x][y])
            # print(x, y, g.get_edge_data(x, y))


# Method Defined to printgraph
def printgraph(g):
    for x, ys in g.adjacency_iter():
        for y, edge in ys.items():
            print('(%s, %s, %f)' % (x, y, edge['weight']))


# Another Method Defined to printgraph
def printedges(g):
    for x, y, z in g.edges(data='weight'):
        print('(%s, %s, %d)' % (x, y, z))

'''
# These are the various In-built methods of Networkx tested on graphs
# nx.draw(g)
# printedges(g)
# print(nx.clustering(g), '\n\n', nx.clustering(g2), '\n\n\n\n')
# print(nx.connected_components(g))
# pprint(nx.degree(g2))
# print(max(nx.degree(g).values()))
# print(nx.degree(g), '\n\n', nx.degree(g2), '\n\n')
# print(nx.average_shortest_path_length(g), '\n\n', nx.average_shortest_path_length(g2), '\n\n')
# print(nx.triangles(g), '\n\n', nx.triangles(g2))
# print(g.get_edge_data())
'''
target.close()

# Opening the other 2 perceptual files
file = open('edgesFlav.csv', 'r', encoding="utf8")
file2 = open('edgesSuperSc.csv', 'r', encoding="utf8")
read = csv.reader(file, delimiter=',')
reading = csv.reader(file2, delimiter=',')

g3 = nx.Graph()  # Creating their graphs
g4 = nx.Graph()
yp = []
for row in read:
    yp.extend(row)
# print(yp)
zp = []

for row in reading:
    zp.extend(row)

'''Adding Edges to Other graphs to compare with g and g2 graphs'''
for row in yp:
    # print(type(row[count]))
    # zz = tuple(row)
    # print(type(row))
    x, y = row.split(',')
    # y = row[count][1]
    xn = x[2:-1]
    yn = y[2:-2]
    # print(xn)
    g3.add_edge(xn, yn, weight=1)
# printgraph(g3)

for row in zp:
    x, y = row.split(',')
    xn = x[2:-1]
    yn = y[2:-2]
    g4.add_edge(xn, yn, weight=1)


# Defined Method of Eigen Values for Compaison of Graph
def select_k(spectrum, minimum_energy=0.9):
    running_total = 0.0
    total = sum(spectrum)
    if total == 0.0:
        return len(spectrum)
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if running_total / total >= minimum_energy:
            return i + 1
    return len(spectrum)

# Calculating laplacian using networkx
laplacian1 = nx.spectrum.laplacian_spectrum(g)
laplacian2 = nx.spectrum.laplacian_spectrum(g3)
k1 = select_k(laplacian1)
k2 = select_k(laplacian2)
k = min(k1, k2)

# Finding similairty using minimum k
similarity = sum((laplacian1[:k] - laplacian2[:k])**2)
print("Similarity[0,inf) in Flavournet Graphs is ", similarity)
# nx.draw(g3)

laplacian3 = nx.spectrum.laplacian_spectrum(g2)
laplacian4 = nx.spectrum.laplacian_spectrum(g4)
k3 = select_k(laplacian3)
k4 = select_k(laplacian4)
k = min(k3, k4)

similarity = sum((laplacian3[:k] - laplacian4[:k])**2)
print("Similarity[0,inf) in Superscent Graphs is ", similarity)
