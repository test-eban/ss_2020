import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

import constantCoords as cc
from algorithms import a_star, bellman_ford, dijkstra, floyd_warshall
from graph import generate_graph_from_city, generate_graph_from_coords, get_area_and_basic_stats

"""Diese Datei ist das Kernstück. Hier befindet sich der Wrapper, welcher dafür zuständig ist, aus Algorithmus-Bezeichnung
und Koordinaten eine Route zu basteln.

Für Informationen, welche Algorithmen gehen und wie die Funktionen aufgerufen werden siehe Beispiele (ggf. auskommentiert) und die Klassenkommentare.

Ich kann nur davor warnen, Floyd-Warshall auf andere Graphen als auf den in test_beispiel() verwendeten loszulassen!
"""

def plan_route_from_coords(name:str, orig_coords: tuple, dest_coords: tuple, show: bool=None):
    """Helper, um Koordinaten als Basis für die plan_route_from_graph(...)-Funktion zu verwenden.
    """
    G = generate_graph_from_coords(orig_coords, dest_coords)
    plan_route_from_graph(name, G, orig_coords, dest_coords, show)

def plan_route_from_city(name:str, city: str, orig_coords: tuple, dest_coords: tuple, show: bool=None):
    """Helper, um einen Stadtnamen als Basis für die plan_route_from_graph(...)-Funktion zu verwenden.
    """
    G = generate_graph_from_city(city)
    plan_route_from_graph(name, G, orig_coords, dest_coords, show)

def plan_route_from_graph(name: str, G, orig_coords, dest_coords, show: bool=None):
    """Diese Funktion wendet einen Algorithmus (name) auf einen Graphen G an, um den besten Weg
    von den Startkoordinaten (orig_coords) zu den Zielkoordinaten (dest_coords) zu ermitteln.
    Steht show auf True, wird der Graph geplottet, ansonsten (auch bei weglassen), werden nur die Daten ausgegeben.

    Zulässige name-Werte (Aufsteigend: ungefähre Laufzeit):
    * a-star
    * dijkstra
    * bellman-ford
    * floyd-warshall
    """
    # fetch nodes and prepare fields
    orig_node = ox.get_nearest_node(G, orig_coords)
    dest_node = ox.get_nearest_node(G, dest_coords)
    
    dist = {}
    pred = {}
    route = []

    if show is None:
        show = False

    print(f"===== START {name}, ({orig_coords[2]} → {dest_coords[2]})")
    if (name == "floyd-warshall"):
        # call algorithm
        dist, next, count = floyd_warshall(G)
        # prepare route
        u = orig_node
        v = dest_node
        while u != v:
            route += [u]
            u = next[u][v]

    else:
        # call algorithm
        if (name == "dijkstra"):
            dist, pred, count = dijkstra(G, orig_node)
        elif (name == "a-star"):
            dist, pred, count = a_star(G, orig_node, dest_node)
        elif (name == "bellman-ford"):
            dist, pred, count = bellman_ford(G, orig_node)
        # prepare route
        v = dest_node
        while v is not None:
            route = [v] + route
            v = pred[v]

    printInfos(G, dist, pred, count, route, dist[dest_node])
    print(f"===== ENDE {name}")

    nc = ['r' if x in dist.keys() else 'black' for x in G.nodes]
    fig, ax = ox.plot_graph_route(G, route, node_size=24, node_color=nc, node_alpha=0.6, route_color='b', route_alpha=0.7, show=show)

def printInfos(G, dist, pred, count, route, length):
    """Dient der strukturierten Informationsausgabe aus den Parametern.
    """
    print(f"= Kanten: {len(G.edges)} \
    \n= Knoten: {len(G)} \
    \n= Besuchte Knoten: {len(dist)} \
    \n= Operationen: {count} \
    \n= Länge der Route (V): {len(route)} \
    \n= Länge der Route (m): {length}")
    # \n= rel. Operationen je besuchter Knoten: {count/len(dist)} \
    # \n= rel. Operationen je Gesamtzahl Knoten: {count/len(G)}")

def execute_evaluation():
    """Diese Funktion erhebt die von mir verwendeten Daten unter Verwendung der anderen Methoden in dieser Datei.
    Es werden die Strecken 1-15 durch die Algorithmen Dijkstra und A-Stern abgelaufen und die Strecke 1 durch den Algorithmus Bellman-Ford.

    Strecken (Kürzel): (Es wird jeweils einmal A → B und B → A durchgeführt als Aufruf)
        1. IS → ISV        6. ISV → HA        10. HA → SO         13. SO → LUE     15. SO → ME
        2. IS → HA         7. ISV → SO        11. HA → LUE        14. LUE → ME
        3. IS → SO         8. ISV → LUE       12. HA → ME
        4. IS → LUE        9. ISV → ME
        5. IS → ME
    """
    # dijkstra
    # 1-5
    plan_route_from_coords('dijkstra', cc.iserlohn, cc.iserlohnVerwaltung)
    plan_route_from_coords('dijkstra', cc.iserlohnVerwaltung, cc.iserlohn)
    plan_route_from_coords('dijkstra', cc.iserlohn, cc.hagen)
    plan_route_from_coords('dijkstra', cc.hagen, cc.iserlohn)
    plan_route_from_coords('dijkstra', cc.iserlohn, cc.soest)
    plan_route_from_coords('dijkstra', cc.soest, cc.iserlohn)
    plan_route_from_coords('dijkstra', cc.iserlohn, cc.luedenscheid)
    plan_route_from_coords('dijkstra', cc.luedenscheid, cc.iserlohn)
    plan_route_from_coords('dijkstra', cc.iserlohn, cc.meschede)
    plan_route_from_coords('dijkstra', cc.meschede, cc.iserlohn)
    # 6-9
    plan_route_from_coords('dijkstra', cc.iserlohnVerwaltung, cc.hagen)
    plan_route_from_coords('dijkstra', cc.hagen, cc.iserlohnVerwaltung)
    plan_route_from_coords('dijkstra', cc.iserlohnVerwaltung, cc.soest)
    plan_route_from_coords('dijkstra', cc.soest, cc.iserlohnVerwaltung)
    plan_route_from_coords('dijkstra', cc.iserlohnVerwaltung, cc.luedenscheid)
    plan_route_from_coords('dijkstra', cc.luedenscheid, cc.iserlohnVerwaltung)
    plan_route_from_coords('dijkstra', cc.iserlohnVerwaltung, cc.meschede)
    plan_route_from_coords('dijkstra', cc.meschede, cc.iserlohnVerwaltung)
    # 10-12
    plan_route_from_coords('dijkstra', cc.hagen, cc.soest)
    plan_route_from_coords('dijkstra', cc.soest, cc.hagen)
    plan_route_from_coords('dijkstra', cc.hagen, cc.luedenscheid)
    plan_route_from_coords('dijkstra', cc.luedenscheid, cc.hagen)
    plan_route_from_coords('dijkstra', cc.hagen, cc.meschede)
    plan_route_from_coords('dijkstra', cc.meschede, cc.hagen)
    # 13-14
    plan_route_from_coords('dijkstra', cc.soest, cc.luedenscheid)
    plan_route_from_coords('dijkstra', cc.luedenscheid, cc.soest)
    plan_route_from_coords('dijkstra', cc.soest, cc.meschede)
    plan_route_from_coords('dijkstra', cc.meschede, cc.soest)
    # 15
    plan_route_from_coords('dijkstra', cc.luedenscheid, cc.meschede)
    plan_route_from_coords('dijkstra', cc.meschede, cc.luedenscheid)

    # a-star
    # 1-5
    plan_route_from_coords('a-star', cc.iserlohn, cc.iserlohnVerwaltung)
    plan_route_from_coords('a-star', cc.iserlohnVerwaltung, cc.iserlohn)
    plan_route_from_coords('a-star', cc.iserlohn, cc.hagen)
    plan_route_from_coords('a-star', cc.hagen, cc.iserlohn)
    plan_route_from_coords('a-star', cc.iserlohn, cc.soest)
    plan_route_from_coords('a-star', cc.soest, cc.iserlohn)
    plan_route_from_coords('a-star', cc.iserlohn, cc.luedenscheid)
    plan_route_from_coords('a-star', cc.luedenscheid, cc.iserlohn)
    plan_route_from_coords('a-star', cc.iserlohn, cc.meschede)
    plan_route_from_coords('a-star', cc.meschede, cc.iserlohn)
    # 6-9
    plan_route_from_coords('a-star', cc.iserlohnVerwaltung, cc.hagen)
    plan_route_from_coords('a-star', cc.hagen, cc.iserlohnVerwaltung)
    plan_route_from_coords('a-star', cc.iserlohnVerwaltung, cc.soest)
    plan_route_from_coords('a-star', cc.soest, cc.iserlohnVerwaltung)
    plan_route_from_coords('a-star', cc.iserlohnVerwaltung, cc.luedenscheid)
    plan_route_from_coords('a-star', cc.luedenscheid, cc.iserlohnVerwaltung)
    plan_route_from_coords('a-star', cc.iserlohnVerwaltung, cc.meschede)
    plan_route_from_coords('a-star', cc.meschede, cc.iserlohnVerwaltung)
    # 10-12
    plan_route_from_coords('a-star', cc.hagen, cc.soest)
    plan_route_from_coords('a-star', cc.soest, cc.hagen)
    plan_route_from_coords('a-star', cc.hagen, cc.luedenscheid)
    plan_route_from_coords('a-star', cc.luedenscheid, cc.hagen)
    plan_route_from_coords('a-star', cc.hagen, cc.meschede)
    plan_route_from_coords('a-star', cc.meschede, cc.hagen)
    # 13-14
    plan_route_from_coords('a-star', cc.soest, cc.luedenscheid)
    plan_route_from_coords('a-star', cc.luedenscheid, cc.soest)
    plan_route_from_coords('a-star', cc.soest, cc.meschede)
    plan_route_from_coords('a-star', cc.meschede, cc.soest)
    # 15
    plan_route_from_coords('a-star', cc.luedenscheid, cc.meschede)
    plan_route_from_coords('a-star', cc.meschede, cc.luedenscheid)
    
    # bellman-ford
    # 1
    plan_route_from_coords('bellman-ford', cc.iserlohn, cc.iserlohnVerwaltung)
    plan_route_from_coords('bellman-ford', cc.iserlohnVerwaltung, cc.iserlohn)

    # floyd-warshall (takes very long)
    # plan_route_from_coords('floyd-warshall', cc.iserlohn, cc.iserlohnVerwaltung)
    # plan_route_from_coords('floyd-warshall', cc.iserlohnVerwaltung, cc.iserlohn)

def test_beispiel(show: bool):
    """Stellt ein Beispiel anhand eines konstruierten Graphes dar, den die Algorithmen Dijkstra, Floyd-Warshall 
    und Bellman-Ford einmal ablaufen. Von jedem Algorithmus werden die Ergebnisse ausgegeben.
    
    A-Stern wurde ausgelassen, da die Haversine Distance nicht mit simplen Knoten funktioniert.
    """
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([1,2,3,4,5])
    graph.add_edge(1,4,length=10)
    graph.add_edge(1,2,length=5)
    graph.add_edge(2,3,length=3)
    graph.add_edge(3,4,length=1)
    graph.add_edge(3,5,length=8)
    graph.add_edge(4,3,length=1)
   
    if(show):
        nx.draw(graph)
        plt.show()

    print("*** DURCHLAUF TEST_BEISPIEL(): ")
    print("""            10 
       (1)------->(4) 
        |         /|\ 
      5 |          | 
        |          | 1 
       \|/         | 
       (2)------->(3)------->(5) 
            3           8
        """)
    print(f"===== START Dijkstra")
    dist, pred, count = dijkstra(graph, 1)
    print(f"= Distanz von Startpunkt zum jeweiligen Key: {dist}".replace("{", "").replace("}",""))
    print(f"= Vorheriger Knoten zum jeweiligen Key: {pred}".replace("{", "").replace("}",""))
    print(f"===== ENDE Dijkstra")

    print(f"===== START Bellman-Ford")
    dist, pred, count = bellman_ford(graph, 1)
    print(f"= Distanz von Startpunkt zum jeweiligen Key: {dist}".replace("{", "").replace("}",""))
    print(f"= Vorheriger Knoten zum jeweiligen Key: {pred}".replace("{", "").replace("}",""))
    print(f"===== ENDE Bellman-Ford")

    print(f"===== START Floyd-Warshall")
    dist, next, count = floyd_warshall(graph)
    result_dist = prepare_matrix_for_printing(dist)
    result_next = prepare_matrix_for_printing(next)
    print("= Distanz von Startpunkt zum jeweiligen Key:")
    print(result_dist)
    print(f"= Nächster Knoten auf dem optimalen Pfad von A (Links) Nach B (Oben):")
    print(result_next)
    print(f"===== ENDE Floyd-Warshall")

    # excluded a-star due to it being unable to use its haversine-distance on flat nodes

def prepare_matrix_for_printing(mat):
    """Diese Funktion hat einen einzigen Zweck: für die test_beispiel-Funktion Matrizen zum printen vorbereiten.
    Dementsprechend unoptimiert und unschön ist sie.
    """
    result = '=  '
    for row in mat.keys():
        result += ('{:4}'.format(row))
    result += '\n'
    for row in mat:
        result += f"= {row}"
        for val in mat[row].values():
            # if val == 'x':
            result += ('{:4}'.format(val).replace("99999", "   ∞").replace("x   ", "   x"))
        result += '\n'

    return result

# test
test_beispiel(show=True)

# plan route from city
plan_route_from_city('a-star', 'Iserlohn, DE', cc.iserlohn, cc.iserlohnVerwaltung, True)

# plan route from coords / dijkstra
plan_route_from_coords(name='dijkstra', orig_coords=cc.iserlohn, dest_coords=cc.hagen, show=True)

# plan route from coords / a-star
plan_route_from_coords('a-star', cc.iserlohn, cc.hagen, True)

# plan route from graph
G = ox.graph_from_place("Iserlohn, DE", network_type='bike')
plan_route_from_graph('dijkstra', G, cc.iserlohn, cc.iserlohnVerwaltung, True)

# execute evaluation -- WARNING: this may take quite some time  
# execute_evaluation()