import sys
import random
import time
import itertools

from tqdm import tqdm, trange


import json
from collections import defaultdict
from multiprocessing import Process,Queue,current_process, freeze_support,Value

sys.path.insert(0,'e:\\python\\data_structures_algorithms\\DataStructures')
from undirected_graph import Undirected_Graph #type: ignore


def create_random_graph(vertexs,max_edges=6):
    
    random_ = random.Random(2020)

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

def multiworker_path_finder_iter_v2(graph,from_vertex,to_vertex,best_path_cost,number_of_processes=4,output_valid_paths=False):
    assert (from_vertex and to_vertex) in graph.keys()

    NUMBER_OF_PROCESSES = number_of_processes

    task_queue = Queue()
    valid_route_queue = Queue()
    best_path_cost_so_far = Value('i',int(best_path_cost))
    best_path = defaultdict(list)

    timestamp = int(time.time())

    task_queue.put([[from_vertex],0])

    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker_iter_v2,args=(graph,to_vertex,task_queue,valid_route_queue,best_path_cost_so_far),daemon=True).start()

    time.sleep(1)
   
    wait_threads = True
    while wait_threads:
        if task_queue.empty() and valid_route_queue.empty():
            wait_threads = False
        elif not valid_route_queue.empty():
            
            while not valid_route_queue.empty():
                v_route,cost = valid_route_queue.get()
                best_path[cost].append(v_route)
        else:
            time.sleep(1)

    assert task_queue.qsize() == 0 , "search did not complete"
    assert valid_route_queue.qsize() ==0, "valid routes remaining"

    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    if output_valid_paths and len(best_path.keys()) > 0:
        with open(f"Search\\valid_paths_from_{from_vertex}_to_{to_vertex}_{timestamp}.txt",'a') as fp:
            for cost,paths in best_path.items():
                for path in paths:
                    fp.write("%s\n" % json.dumps(dict(path=path,cost=cost)))

    #print("threads stopping")

    task_queue.close()
    valid_route_queue.close()
    
    if len(best_path.keys()) > 0:
        bpc = min(best_path.keys())
        return  bpc,best_path[bpc]
    else:
        return int(best_path_cost_so_far.value),None
    
def best_path_visit_all_nodes_once():
    graph = random_graph()
    
    l = len(graph)

    valid_best_paths = defaultdict(list)

    best_path_cost = 99999

    with tqdm(total=l*l) as pbar:
        for from_vertex in graph.keys():
            for to_vertex in graph.keys():
                
                pbar.update()
                if from_vertex == to_vertex:
                    continue
                best_path_cost,best_paths = multiworker_path_finder_iter_v2(graph,from_vertex,to_vertex,best_path_cost,number_of_processes=6,output_valid_paths=True)
                
                if best_paths is not None:
                    for path in best_paths:
                        valid_best_paths[best_path_cost].append(path)

    if len(valid_best_paths.keys()) == 0:
        return None
    else:
        bpc = min(valid_best_paths.keys())
        return bpc,valid_best_paths[bpc]
    
            
if __name__ == "__main__":
    freeze_support()

    print(best_path_visit_all_nodes_once())