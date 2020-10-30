
import time
from collections import defaultdict,deque
from multiprocessing import Process, Queue,current_process,freeze_support

from heap import MinHeap # type: ignore

class Undirected_Graph:

    def __init__(self):

        self._graph_dict = defaultdict(set)

    def getVertices(self):

        return list(self._graph_dict.keys())

    def addVertice(self,vertex):
        if vertex not in self._graph_dict.keys():
            self._graph_dict[vertex]

    def addEdge(self,from_vertex,to_vertex,cost=1):
        assert (from_vertex and to_vertex) in self._graph_dict.keys()

        self._graph_dict[from_vertex].add((to_vertex,cost))
        self._graph_dict[to_vertex].add((from_vertex,cost))
    
    def isAdjacent(self,from_vertex,to_vertex):
        if to_vertex in list(vertex for vertex,_ in self._graph_dict[from_vertex]):
            return True

        return False

    def getNeighbors(self,vertex):
        assert vertex in self._graph_dict.keys()

        return self._graph_dict[vertex]

    def findEdges(self):
    
        unique_edges = []

        for vertex in self._graph_dict.keys():
            for edge,_ in self._graph_dict[vertex]:

                if {vertex,edge} not in unique_edges:
                    unique_edges.append({vertex,edge})

        return unique_edges

    def all_paths(self,from_vertex,to_vertex):
    
        assert (from_vertex and to_vertex) in self._graph_dict.keys()

        queue = [[from_vertex]]

        
        routes = []

        if from_vertex == to_vertex:
            print("From and To node are the same")
            return

        while queue:
            #print(len(queue))
            path = queue.pop(0)
            node = path[-1]

            neighbors = self.getNeighbors(node)

            for neighbor,cost in neighbors:
     
                new_path = list(path)
                
                if neighbor in new_path:
                    continue

                new_path.append(neighbor)
                queue.append(new_path)

                if neighbor == to_vertex:
                    routes.append(new_path)

        return routes



  




