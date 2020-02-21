from math import radians, cos, sin, asin, sqrt
import heapq

"""Diese Datei stellt immer wieder gebrauchte Funktionen zur Verfügung, die keinem spezifischen Bereich zugehörig sind
"""

# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

class PriorityQueue:
    """Implementierung einer PriorityQueue mit Hilfe von heapq.
    heapq verwaltet einen Heap, d.h. eine Liste von numerischen Werten mit schnellem Zugriff auf das 
    kleinste Element.
    
    Übernommen von Prof. Gawron. Geänderte Inhalte gekennzeichnet.
    """

    def __init__(self):
        self._queue = []
        self._index = 0

    def __len__(self):
        return self._index
    
    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        
    def pop(self):
        """Gibt das Element mit der kleinsten Priorität zurück."""
        self._index -= 1
        return heapq.heappop(self._queue)[-1]

    def show(self): # hinzugefügt
        print(self._queue)

    def is_in(self, x): # hinzugefügt
        return self.index(x) != -1

    def index(self, x): # hinzugefügt
        for elem in self._queue:
            if x == elem[2]:
                self._queue.index(elem)
        return -1

    def update(self, item, priority): # hinzugefügt
        index = self.index(item)
        if index != -1:
            self._queue.pop(index)
            heapq.heapify(self._queue)
            self.push(item, priority)