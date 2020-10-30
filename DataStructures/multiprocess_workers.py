import sys
import random
import time
import itertools

from tqdm import tqdm


import json
from collections import defaultdict
from multiprocessing import Process,Queue,current_process, freeze_support,Value

def _transverse_all_vertexes_once_bound_by_cost(path,total_cost,neighbors,to_vertex,min_path_cost,num_vertexs):
    
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

def _transverse_vertexes_once_to_vertex(path,total_cost,neighbors,to_vertex,*_):
    retval = []
    valid_paths = []

    for neighbor,cost in neighbors:
                    
        new_path = list(path)
        new_cost = total_cost + cost
        # if needed check for repeat condition

        if neighbor in new_path:
            continue

        new_path.append(neighbor)

        if neighbor == to_vertex:
            valid_paths.append([new_path,new_cost])
            continue

        retval.append([new_path,new_cost])

    return retval,valid_paths

def _worker(graph,to_vertex,task_function,task_q,valid_routes_q,b_path):
    
    # print(f"{current_process().name}: started")
    
    n_vertexs = len(graph)

    for path,total_cost in iter(task_q.get,'STOP'):
  
        node = path[-1]
        neighbors = graph[node]

        new_paths,valid_routes = task_function(path,total_cost,neighbors,to_vertex,int(b_path.value),n_vertexs)

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

def _multiworker_manager(graph,task_function,from_vertex,to_vertex,best_path_cost,number_of_processes=4,output_valid_paths=False):
    assert (from_vertex and to_vertex) in graph.keys()

    NUMBER_OF_PROCESSES = number_of_processes

    task_queue = Queue()
    valid_route_queue = Queue()
    best_path_cost_so_far = Value('i',int(best_path_cost))
    best_paths = defaultdict(list)

    timestamp = int(time.time())

    task_queue.put([[from_vertex],0])

    for _ in range(NUMBER_OF_PROCESSES):
        Process(target=_worker,args=(graph,to_vertex,task_function,task_queue,valid_route_queue,best_path_cost_so_far),daemon=True).start()

    time.sleep(1)
   
    wait_threads = True
    while wait_threads:
        if task_queue.empty() and valid_route_queue.empty():
            wait_threads = False
        elif not valid_route_queue.empty():
            
            while not valid_route_queue.empty():
                v_route,cost = valid_route_queue.get()
                best_paths[cost].append(v_route)
        else:
            time.sleep(1)

    assert task_queue.qsize() == 0 , "search did not complete"
    assert valid_route_queue.qsize() ==0, "valid routes remaining"

    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    if output_valid_paths and len(best_paths.keys()) > 0:
        with open(f"Search\\valid_paths_from_{from_vertex}_to_{to_vertex}_{timestamp}.txt",'a') as fp:
            for cost,paths in best_paths.items():
                for path in paths:
                    fp.write("%s\n" % json.dumps(dict(path=path,cost=cost)))

    #print("threads stopping")

    task_queue.close()
    valid_route_queue.close()
    # print(best_paths)
    return int(best_path_cost_so_far.value),best_paths
    
def best_path_visit_all_nodes_once(graph,number_of_processes=2):
  
    l = len(graph)

    valid_best_paths = defaultdict(list)

    best_path_cost = 99999

    task_function = _transverse_all_vertexes_once_bound_by_cost

    with tqdm(total=l*l) as pbar:
        for from_vertex in graph.keys():
            for to_vertex in graph.keys():
                
                pbar.update()
                if from_vertex == to_vertex:
                    continue
                best_path_cost,best_paths = _multiworker_manager(graph,task_function,from_vertex,to_vertex,best_path_cost,number_of_processes=number_of_processes,output_valid_paths=True)
                
                if best_paths:
                    for cost,paths in best_paths.items():
                        list(valid_best_paths[cost].append(path) for path in paths)

    if valid_best_paths:

        bpc = min(valid_best_paths.keys())
        return bpc,valid_best_paths[bpc]

def from_to_vertex_visit_nodes_only_once(graph,from_vertex,to_vertex,number_of_processes=2):

    best_path_cost = 99999

    task_function = _transverse_vertexes_once_to_vertex

    best_path_cost,valid_best_paths = _multiworker_manager(graph,task_function,from_vertex,to_vertex,best_path_cost,number_of_processes=number_of_processes,output_valid_paths=True)
    unwrapped_paths = [(key,path) for key,paths in valid_best_paths.items() for path in  paths]
    min_len = min(map(lambda x: len(x[1]),unwrapped_paths))
    max_len = max(map(lambda x: len(x[1]),unwrapped_paths))
    min_cost = min(valid_best_paths.keys())
    max_cost = max(valid_best_paths.keys())
    return {
        'shortest': [(path,key) for key,path in unwrapped_paths if len(path) == min_len],
        'longest':[(path,key) for key,path in unwrapped_paths if len(path) == max_len],
        'least cost':(valid_best_paths[min_cost],min_cost),
        'highest cost': (valid_best_paths[max_cost],max_cost)
    }

if __name__ == "__main__":
    freeze_support()

    print(best_path_visit_all_nodes_once())