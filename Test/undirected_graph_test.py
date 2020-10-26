import sys
import random
import time
import itertools


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

        retval.append([new_path,cost])

    return retval,valid_paths


def worker_iter_v2(graph,to_vertex,task_q,valid_routes_q,best_path_so_far):
    
    print(f"{current_process().name}: started")
    
    n_vertexs = len(graph)

    for path,total_cost in iter(task_q.get,'STOP'):
  
        node = path[-1]
        neighbors = graph[node]

        new_paths,valid_routes = transverse_all_paths(path,total_cost,neighbors,to_vertex,best_path_so_far.value,n_vertexs)

        if len(new_paths) > 0:
            for new_path in new_paths:
                task_q.put(new_path)

        if len(valid_routes)>0:
            for valid_route in valid_routes:
                _,cost = valid_route
                if cost < best_path_so_far.value:
                    best_path_so_far.value = cost
                valid_routes_q.put(valid_route)
       
    print(f"{current_process().name}: stopped")

def multiworker_path_finder_iter_v2(graph,from_vertex,to_vertex,number_of_processes=4):
    assert (from_vertex and to_vertex) in graph.keys()

    NUMBER_OF_PROCESSES = number_of_processes

    task_queue = Queue()
    valid_route_queue = Queue()
    best_path_so_far = Value('i',99999)

    timestamp = int(time.time())

    task_queue.put([[from_vertex],0])

    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker_iter_v2,args=(graph,to_vertex,task_queue,valid_route_queue,best_path_so_far),daemon=True).start()


    time.sleep(1)
   
    def wait_for_threads():
        wait_threads = True
        while wait_threads:
            if task_queue.empty():
                wait_threads = False

            if valid_route_queue.qsize() > 0:
                with open(f"valid_paths_from_{from_vertex}_to_{to_vertex}_{timestamp}.txt",'a') as fp:
                    while not valid_route_queue.empty():
                        v_route,cost = valid_route_queue.get()
                        
                        fp.write("%s\n" % json.dumps(dict(path=v_route,cost=cost)))
        
        time.sleep(3)


    while True:
        if not task_queue.empty():
            wait_for_threads()
        else:
            break


        
    
    print(f"task queue empty {task_queue.qsize()} , stopping threads")
    assert task_queue.qsize() == 0 , "search did not complete"
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

 
    print("threads stopping")





    #print(valid_route_queue.qsize())
            

def transverse_node(path,total_cost,to_vertex,neighbors,need_to_visit):
    visited = set(path)

    

    found_path = []
    ret = []
    diff = need_to_visit.symmetric_difference(visited) # remaining vertex still needed to be visited
    
    for neighbor,cost in neighbors:
                
        new_path = list(path)
        new_cost = total_cost + cost
        # if needed check for repeat condition

        if neighbor in new_path or new_cost > 500:
            continue

        new_path.append(neighbor)
        
        #change later
        if neighbor == to_vertex and len(diff)<10:
            found_path.append([new_path,new_cost])
            continue
        
        ret.append([new_path,cost])
            
    return ret,found_path

def worker_iter_v1(graph,to_vertex,task_q,feeder_q,routes_q):
    need_to_visit = set(graph.keys())
    print(f"starting thread {current_process().name}: ")

    for path,total_cost in iter(task_q.get,'STOP'):
        node = path[-1]
        new_paths,routes = transverse_node(path,total_cost,to_vertex,graph[node],need_to_visit)

        if len(new_paths) > 0:
            for new_path in new_paths:
                feeder_q.put(new_path)

        if len(routes) > 0:
            for route in routes:
                routes_q.put(route)
      
def multiworker_path_finder_iter_v1(graph,from_vertex,to_vertex,number_of_processes=4):
    assert (from_vertex and to_vertex) in graph.keys()

    NUMBER_OF_PROCESSES = number_of_processes

    task_queue = Queue()
    routes_queue = Queue()
    #feeder_queues = {}
    feeder_queue = Queue()
    
    task_queue.put([[from_vertex],0])

    running = True
    debug_iter = itertools.count()



    # #start threads
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker_iter_v1,args=(graph,to_vertex,task_queue,feeder_queue,routes_queue),daemon=True).start()
    time.sleep(1)

    def process():
        while not feeder_queue.empty():
            i = next(debug_iter)
            for _ in range(feeder_queue.qsize()):
                task_queue.put(feeder_queue.get())
                
            # if i % 100 == 0:
            print(f"iteration: {i} : ",feeder_queue.qsize())
        
        time.sleep(2)

    while running:
        if task_queue.empty() and feeder_queue.empty():
            running = False
        else:
            process()
        

    print(task_queue.qsize(),feeder_queue.qsize())
         
        
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')




    print("main process done stopping threads")

    print(routes_queue.qsize())
            
 


if __name__ == "__main__":
    freeze_support()
    #exit(multiworker_path_finder_iter_v1(random_graph(),'A','Z',number_of_processes=6))

    start =  time.time_ns()
    multiworker_path_finder_iter_v2(random_graph(),'K','O',number_of_processes=6)

    print((time.time_ns() - start)*1e-9)