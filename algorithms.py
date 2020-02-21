from collections import defaultdict
import networkx as nx

from utility import PriorityQueue, haversine

INF = 99999

""" Alle Methoden sind so angelegt, dass sie den Graphen und ggf. Start- und Endknoten annehmen.
dijkstra, a_star und bellman_ford geben 2 Dictionaries zurück, die zu jeden Punkt den Vorgänger und den Abstand enthalten
sowie die Anzahl der inneren Durchläufe. Es werden die Durchläufe gezählt und nicht die einzelnen Operationen. Daher der 
Unterschied zu der im Dokument angegebenen Komplexitätsangabe. Ignorierte Knoten werden nicht als Durchlauf gezählt. 

Ich kann nur davor warnen, Floyd-Warshall auf andere Graphen als das Beispiel in Evaluation loszulassen!

floyd_warshall gibt 2 Matrizen zurück. Die erste enthält die Entfernung, die zweite den nächsten Knoten auf dem Weg zum Ziel. Für ein Beispiel siehe die Ausarbeitung, Punkt III.4.
"""


def dijkstra(G, p):
    """Der Dijkstra-Algorithmus bestimmt den Abstand aller Punkte von einem Startpunkt aus.
    Rückgabe ist ein dictionary, das zu jedem Punkt den Abstand und den Vorgänger enthält.
    
    Übernommen von Prof. Gawron und lediglich Benennung angepasst.
    """

    dist = dict()
    pred = dict()
    
    pq = PriorityQueue()
    
    # Initialisierung: Der Startpunkt hat Abstand 0 und keinen Vorgänger
    pq.push(p, 0)
    dist[p] = 0
    pred[p] = None
    
    count = 1
    # Wähle den Punkt mit dem kleinsten Abstand und aktualisiere von ihm aus die Abstände
    while len(pq) > 0:
        u = pq.pop()
        for v in nx.neighbors(G, u):
            count += 1 
            length = G[u][v][0]['length']
            
            if (v not in dist) or (dist[u] + length < dist[v]):
                count += 1 
                # Kürzeren Weg nach r gefunden
                dist[v] = dist[u] + length
                pred[v] = u
                pq.push(v, dist[v])
    
    return dist, pred, count

def a_star(G, start, dest):
    """Der A-Stern-Algorithmus versucht, den optimalen Weg zwischen start und dest zu ermitteln, indem er den Weg verfolgt, der *wahrscheinlich* zum Ziel führt.
    """
    # initialize fields
    openlist = PriorityQueue()
    closedset = set()
    dist = dict()
    pred = dict()
    
    # add root-node
    openlist.push(start, 0)
    dist[start] = 0
    pred[start] = None
    
    count = 0
    while len(openlist) >= 0: # while openlist is not empty
        u = openlist.pop() # get node from openlist
        if u == dest: 
            return dist, pred, count # destination reached
        
        closedset.add(u) 

        for v in nx.neighbors(G, u): # for each neighbour of u
            if v in closedset: # v already found and checked
                continue
            # v has not been "found" yet
            count += 1

            length = G[u][v][0]['length']  # get length of edge[u][v]
            tentative_g = dist[u] + length # get length from start to v

            if v in dist and tentative_g >= dist[v]: # if has a distance and if this distance is smaller than the possible new distance - continue
                continue
            # else - v is not yet in dist[] or the possible new distance is smaller than the saved distance
            pred[v] = u # (new) predecessor of v is u
            dist[v] = tentative_g # (new) dist from start to v is tentative_g

            h = haversine(G.nodes[v]['y'], G.nodes[v]['x'], G.nodes[dest]['y'], G.nodes[dest]['x'])*1000 # get predicted distance
            f = tentative_g + h # add predicted distance to existing distance

            if openlist.is_in(v): # if v has already been discovered (= exists in the openlist) update its predicted distance
                openlist.update(v, f)
            else: # else add it with its predicted distance
                openlist.push(v, f)

    return dist, pred, count

def bellman_ford(G, start):
    """Der Bellman-Ford-Algorithmus ermittelt zu jedem Punkt den kürzesten Weg, ähnlich dem Dijkstra-Algorithmus. 
    Allerdings kann der Bellman-Ford-Algorithmus auch mit negativen Kantengewichtungen umgehen.
    """
    # initialize fields
    dist = dict()
    pred = dict()
    for node in G:
        dist[node] = INF
        pred[node] = None
    # set start = 0
    dist[start] = 0
    pred[start] = None

    count = 0
    for i in range(len(G.nodes)): # for the amount of nodes in G
        for edge in G.edges: # visit all edges
            count += 1
            u = edge[0]
            v = edge[1]
            length = G[u][v][0]['length']
            # RELAX
            if dist[v] > dist[u] + length:
                dist[v] = dist[u] + length
                pred[v] = u

    # check for negative weight cycles
    for node in G:
        for v in nx.neighbors(G, u):
            assert dist[v] <= dist[u] + G[u][v][0]['length'], "Negative weight cycle."

    # if none are found the result is valid
    return dist, pred, count

def floyd_warshall(G):
    """Der Floyd-Warshall-Algorithmus findet die kürzesten Pfade zwischen *allen* Knotenpaaren eines Graphes mitsamt der jeweiligen Pfadlänge. 
    Dabei werden unerreichbare Graphen mit 'x' gekennzeichnet. Laufzeittechnisch schwierig.
    """
    # preparing the matrix
    dist = defaultdict(dict)
    next = defaultdict(dict)

    for u in G.nodes:
        for v in G.nodes:
            dist[u][v] = INF
            next[u][v] = 'x'

    # the distance from A to A is 0, from B to B 0 ...
    for i in dist.keys():
        dist[i][i] = 0

    # for each edge in G get u, v, length and save the values in the matrix
    for edge in G.edges:
        u = edge[0]
        v = edge[1]
        dist[u][v] = G[u][v][0]['length']
        next[u][v] = v

    max = len(dist.keys())*len(dist.keys())*len(dist.keys()) # get amount of operations and initialize counter
    count = 0

    # main-part of the Floyd-Warshall-Algorithm
    # for i, j, k -- using dist.keys() to make sure freely named/ numbered nodes can be used too
    for i in dist.keys():
        for j in dist.keys():
            for k in dist.keys():
                if (count) % 10000000 == 0: # trust me, this is needed
                    print("{0} / {1}: {2}".format(count, max, count/max))
                possibleNewLow = dist[i][k] + dist[k][j]
                if dist[i][j] > possibleNewLow:
                    dist[i][j] = possibleNewLow
                    next[i][j]  = next[i][k]
                count += 1

    return dist, next, count

def nx_shortest_path(G, orig_node, dest_node, weight):
    return nx.shortest_path(G, orig_node, dest_node, weight=weight)
