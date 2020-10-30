import sys
import random
import time
import itertools


import json
from collections import deque
from multiprocessing import freeze_support




sys.path.insert(0,'e:\\python\\data_structures_algorithms\\DataStructures')
from undirected_graph import Undirected_Graph #type: ignore
from multiprocess_workers import best_path_visit_all_nodes_once,from_to_vertex_visit_nodes_only_once #type: ignore

def create_random_edges(vertexs,max_edges=6):
    
    random_ = random.Random(1234)

    graph = {}

    for _ in range(len(vertexs)):
        vert = vertexs.pop(0)

        
        n_edges =random_.randint(0,min(max_edges,len(vertexs)))
        edges = random_.sample(vertexs,n_edges)

        edges_cost = [(edge,random_.randint(60,180)) for edge in edges]

        #assert edges_cost[-1] > 0

        if len(vertexs) > 0 and vertexs[0] not in edges: # ensures atleast one path exsist from A to Z with max cost
            edges_cost.append((vertexs[0],300))


        graph[vert]=edges_cost

    return graph

def random_graph():
    graph = Undirected_Graph()
    [graph.addVertice(chr(i)) for i in range(ord('A'),ord('K')+1)]

    
    graph_d = create_random_edges(graph.getVertices())

    for from_vertex,v in graph_d.items():
        if len(v) > 0:
            for to_vertex,cost in v:
                graph.addEdge(from_vertex,to_vertex,cost)

    return dict(graph._graph_dict)

def find_all_paths_class_function():

    graph = Undirected_Graph()
    [graph.addVertice(chr(i)) for i in range(ord('A'),ord('K')+1)]

    
    graph_d = create_random_edges(graph.getVertices())

    for from_vertex,v in graph_d.items():
        if len(v) > 0:
            for to_vertex,cost in v:
                graph.addEdge(from_vertex,to_vertex,cost)

    print(graph.all_paths('A','K'))

def find_best_path_visit_all_nodes():
    graph = random_graph()

    result = best_path_visit_all_nodes_once(graph,number_of_processes=6)
    print(result)

def find_best_path_from_vertex_and_to_vertex():
    graph = random_graph()

    result = from_to_vertex_visit_nodes_only_once(graph,'A','K',number_of_processes=6)
    print(result)

if __name__ == "__main__":
    # freeze_support()
    #exit(multiworker_path_finder_iter_v1(random_graph(),'A','Z',number_of_processes=6))

    start =  time.time_ns()
    #find_all_paths_class_function()
    #find_best_path_visit_all_nodes()
    find_best_path_from_vertex_and_to_vertex()
    print((time.time_ns() - start)*1e-9)