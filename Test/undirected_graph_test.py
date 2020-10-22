import sys
import random
sys.path.insert(0,'e:\\python\\data_structures_algorithms\\DataStructures')

from undirected_graph import Undirected_Graph #type: ignore


def create_random_graph(vertexs,max_edges=2):
    
    random_ = random.Random(1337)

    graph = {}

    for _ in range(len(vertexs)):
        vert = vertexs.pop(0)

        
        n_edges =random_.randint(0,min(max_edges,len(vertexs)))
        edges = random_.sample(vertexs,n_edges)

        edges_cost = [(edge,random_.randint(60,180)) for edge in edges]


        if len(vertexs) > 0 and vertexs[0] not in edges: # ensures atleast one path exsist from A to Z with max cost
            edges_cost.append((vertexs[0],300))


        graph[vert]=edges_cost

    return graph

def random_graph():
    graph = Undirected_Graph()
    [graph.addVertice(chr(i)) for i in range(ord('A'),ord('Z')+1)]

    
    graph_d = create_random_graph(graph.getVertices())

    for from_vertex,v in graph_d.items():
        if len(v) > 0:
            for to_vertex,cost in v:
                graph.addEdge(from_vertex,to_vertex,cost)

    #print(graph.findEdges())
    #print(graph.adjacent('A','M'))

    #print(graph.all_paths('A','D'))
    
    #result = graph.all_paths_bound_by_cost('K','T',1000)

    #print(result,len(result))


    graph.visit_each_node_with_least_cost('K','T',)
random_graph()