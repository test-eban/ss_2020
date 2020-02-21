import osmnx as ox

"""
Diese Datei stellt alle Graphen-relevanten Funktionen bereit. 
So lassen sich mit diesen Funktionen Graphen aus:
    - Städten
    - Koordinaten und
    - Adressen 
erstellen.
"""

# ox.config(use_cache=True, log_console=True)

graphs = {}

def generate_graph_from_city(city: str):
    """Prüft, ob bereits ein Graph zu der angegebenen Stadt existiert und holt diesen oder erstellt diesen je nachdem.
    """
    if graphs.get(city, "-1") != "-1":
        print("**** graph fetched ****")
        return graphs[city]
    else:
        G = ox.graph_from_place(city, network_type='drive')
        graphs[city] = G
        print("**** graph created ****")
        return G

def generate_graph_from_coords(orig_coords: tuple, dest_coords: tuple):
    """Prüft, ob bereits ein Graph zu den angegebenen Koordinaten existiert und holt diesen oder erstellt diesen je nachdem. 
    Der Graph enthält mind. die Koordinaten sowie ein wenig Abstand zum Rand von den Koordinaten aus.
    """
    key = str(hash(orig_coords[0] + dest_coords[0] + orig_coords[1] + dest_coords[1]))
    if graphs.get(key, "-1") != "-1":
        print("**** graph fetched ****")
        return graphs[key]
    else:
        # using this, the bbox gets slighty bigger resulting in a more usable graph
        if orig_coords[0] > dest_coords[0]:
            north = orig_coords[0] * 1.00015
            south = dest_coords[0] * 0.99985
        else:        
            north = dest_coords[0] * 1.00015
            south = orig_coords[0] * 0.99985

        if orig_coords[1] > dest_coords[1]:
            west = dest_coords[1] * 0.9993
            east = orig_coords[1] * 1.0007
        else:
            west = orig_coords[1] * 0.9993
            east = dest_coords[1] * 1.0007

        G = ox.graph_from_bbox(north, south, east, west)
        graphs[key] = G
        print("**** graph created ****")
        return G

def generate_graph_from_address(address: str, distance: int):
    """Prüft, ob bereits ein Graph zu der angegebenen Adresse existiert und holt diesen oder erstellt diesen je nachdem.
    Die distance bestimmt die Größe des Ergebnisgraphen.
    """
    key = address + str(distance) + '-add'
    if graphs.get(key, "-1") != "-1":
        print("**** graph fetched ****")
        return graphs[key]
    else:
        G = ox.graph_from_address(address=address, distance=distance)
        graphs[key] = G
        print("**** graph created ****")
        return G

def get_area_and_basic_stats(graph):
    """
    Gibt Fläche in km2 an und holt sich Daten zum Graphen.
    """
    G_proj = ox.project_graph(graph)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
    graph_area_m = nodes_proj.unary_union.convex_hull.area

    return graph_area_m / 1000000, ox.basic_stats(G_proj, area=graph_area_m, clean_intersects=True, circuity_dist='euclidean')

def plot_graph(graph, height):
    """Plottet einen Graphen. Ungenutzt.
    """
    fig, ax = ox.plot_graph(graph, fig_height=height)