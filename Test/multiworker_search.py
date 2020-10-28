import sys
import random
import time
import itertools

from tqdm import tqdm, trange


import json
from collections import deque
from multiprocessing import Process,Queue,current_process, freeze_support,Value




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

        #assert edges_cost[-1] > 0

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

    return dict(graph._graph_dict)

def transverse_all_paths(path,total_cost,neighbors,to_vertex,min_path_cost,num_vertexs):

    retval = []
    valid_paths = []

    for neighbor,cost in neighbors:
                    
        new_path = list(path)
        new_cost = total_cost + cost
        # if needed check for repeat condition

        if neighbor in new_path or new_cost > min_path_cost:
            continue

        new_path.append(neighbor)

        if neighbor == to_vertex:
            if len(new_path) ==num_vertexs: # visit every vertex
                valid_paths.append([new_path,new_cost])
            continue

        retval.append([new_path,new_cost])

    return retval,valid_paths

def worker_iter_v2(graph,to_vertex,task_q,valid_routes_q,b_path):
    
    # print(f"{current_process().name}: started")
    
    n_vertexs = len(graph)

    for path,total_cost in iter(task_q.get,'STOP'):
  
        node = path[-1]
        neighbors = graph[node]

        new_paths,valid_routes = transverse_all_paths(path,total_cost,neighbors,to_vertex,int(b_path.value),n_vertexs)

        if len(new_paths) > 0:
            for new_path in new_paths:
                #print(new_path)
                task_q.put(new_path)

        if len(valid_routes)>0:
            for valid_route in valid_routes:
                _,cost = valid_route
                with b_path.get_lock():
                    if b_path.value > cost:
                        b_path.value = cost
                valid_routes_q.put(valid_route)
       
    # print(f"{current_process().name}: stopped")

def multiworker_path_finder_iter_v2(graph,from_vertex,to_vertex,best_path,number_of_processes=4):
    assert (from_vertex and to_vertex) in graph.keys()

    NUMBER_OF_PROCESSES = number_of_processes

    task_queue = Queue()
    valid_route_queue = Queue()
    best_path_so_far = Value('i',int(best_path))

    timestamp = int(time.time())

    task_queue.put([[from_vertex],0])

    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker_iter_v2,args=(graph,to_vertex,task_queue,valid_route_queue,best_path_so_far),daemon=True).start()

    time.sleep(1)
   
    wait_threads = True
    while wait_threads:
        if task_queue.empty() and valid_route_queue.empty():
            wait_threads = False
        elif not valid_route_queue.empty():
            with open(f"Search\\valid_paths_from_{from_vertex}_to_{to_vertex}_{timestamp}.txt",'a') as fp:
                    while not valid_route_queue.empty():
                        v_route,cost = valid_route_queue.get()
                        fp.write("%s\n" % json.dumps(dict(path=v_route,cost=cost)))
        else:
            # print("taske queue: ",task_queue.qsize(),valid_route_queue.qsize())
            time.sleep(1)

    # print(f"task queue empty {task_queue.qsize()} , stopping threads")
    assert task_queue.qsize() == 0 , "search did not complete"
    assert valid_route_queue.qsize() ==0, "valid routes remaining"

    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    print("threads stopping")

    task_queue.close()
    valid_route_queue.close()
    #print(best_path_so_far.value)
    return  int(best_path_so_far.value)
    



def best_path_visit_all_nodes_once():
    graph = random_graph()
    
    l = len(graph)
    best_path = 5000

    test_vertex = ['B','Z','K','C']

    with tqdm(total=l*len(test_vertex)) as pbar:
        for from_vertex in graph.keys():
            for to_vertex in test_vertex:
                # print(from_vertex,to_vertex)
                pbar.update()
                if from_vertex == to_vertex:
                    continue
                best_path = multiworker_path_finder_iter_v2(graph,from_vertex,to_vertex,best_path,number_of_processes=6)
                
        
            break
if __name__ == "__main__":
    freeze_support()

    best_path_visit_all_nodes_once()