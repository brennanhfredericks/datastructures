import pprint
from collections import defaultdict


pp = pprint.PrettyPrinter(indent=4)

#ToDo Implement shortest path

#undirected graph i.e. edge {'a','b'} == edge {'b','a'}
class Graph:

    def __init__(self,graph_dict=None):
        
        self._graph_dict = defaultdict(set)
        
        if graph_dict is None:
            return 
        
        assert type(graph_dict) == dict

        for k,v in graph_dict.items():
            self._graph_dict[k] = set(v)
    
    def getVertices(self):
        
        return list(self._graph_dict.keys())

    def addVertice(self,vertex):

        if vertex not in self._graph_dict.keys():
            self._graph_dict[vertex]

    def addEdge(self,from_vertex,to_vertex):
        assert (from_vertex and to_vertex) in self._graph_dict.keys()

        self._graph_dict[from_vertex].add(to_vertex)
        self._graph_dict[to_vertex].add(from_vertex)
    
    def getEdges(self):
        
        return self.findEdges()#list(self._graph_dict.values())

    def adjacent(self,from_vertex,to_vertex):

        if to_vertex in self._graph_dict[from_vertex]:
            return True

        return False

    def neighbors(self,vertex):
        assert vertex in self._graph_dict.keys()

        return self._graph_dict[vertex]
    
    def remove_vertex(self,vertex):
        assert vertex in self._graph_dict.keys()

        for edge in self._graph_dict[vertex]:
            self._graph_dict[edge].remove(vertex)

        del self._graph_dict[vertex]

    def remove_edge(self,from_vertex,to_vertex):
        assert (from_vertex and to_vertex) in self._graph_dict.keys()

        self._graph_dict[from_vertex].remove(to_vertex)
        self._graph_dict[to_vertex].remove(from_vertex)

    def findEdges(self):

        unique_edges = []

        for vertex in self._graph_dict.keys():
            for edge in self._graph_dict[vertex]:

                if {vertex,edge} not in unique_edges:
                    unique_edges.append({vertex,edge})

        return unique_edges


    def viewGraph(self):

        pp.pprint(self._graph_dict)


