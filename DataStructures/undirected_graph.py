
import time
from collections import defaultdict,deque
from multiprocessing import Process, Queue,current_process,freeze_support

from heap import MinHeap # type: ignore

#Priority Queue
class MinHeap:
    #[[path,cost]]
    def __init__(self):
        self._heap =[[None,None]]

    def peek(self):
        if len(self._heap) > 2:
            return self._heap[1]
        else:
            return False

    def push(self,data):
        self._heap.append(data)
        self._shift_up(len(self._heap)-1)

    def pop(self):
        ret = None

        if len(self._heap) > 2:
            self._swap(1,len(self._heap)-1)
            ret = self._heap.pop()
            self._shift_down(1)

        elif len(self._heap) == 2:
            ret = self._heap.pop()

        return ret

    def size(self):
        return len(self._heap)-1

    def _swap(self,i,j):
        self._heap[i],self._heap[j] = self._heap[j],self._heap[i]

    def _shift_up(self,index):
        parent = index//2

        if index <=1:
            return
        elif self._heap[parent][-1] > self._heap[index][-1]: # check on cost parameter [[]]
            self._swap(parent,index)
            self._shift_up(parent)

    def _shift_down(self,index):

        left_child = 2*index
        right_child = 2*index + 1

        lowest_key = index

        
        if len(self._heap) > left_child and self._heap[lowest_key][-1] > self._heap[left_child][-1]:# check on cost parameter [[]]
            lowest_key = left_child

        if len(self._heap) > right_child and self._heap[lowest_key][-1] > self._heap[right_child][-1]:# check on cost parameter [[]]
            lowest_key = right_child

        if index != lowest_key:
            self._swap(index,lowest_key)
            self._shift_down(lowest_key)  



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

    def all_paths_bound_by_cost(self,from_vertex,to_vertex,cost_bound):
        
        assert (from_vertex and to_vertex) in self._graph_dict.keys()

       # queue = []
        min_queue = MinHeap()

        min_queue.push([[from_vertex],0])

        routes = []

        if from_vertex == to_vertex:
            print("From and To node are the same")
            return

        # print(min_queue.size())
        while min_queue.size() > 0:
            #print(len(queue))
            path,total_cost = min_queue.pop()
            node = path[-1]

            neighbors = self.getNeighbors(node)

            for neighbor,cost in neighbors:
     
                new_path = list(path)
                new_cost = total_cost + cost
                if neighbor in new_path or new_cost > cost_bound:
                    continue

                new_path.append(neighbor)
                min_queue.push([new_path,new_cost])

                if neighbor == to_vertex:
                    routes.append([new_path,new_cost])

        return routes

    def visit_each_node_with_least_cost(self,from_vertex,to_vertex):
        """
        visit each node starting from_vertex and ending at to_vertex in the most cost effective manner:

        - bounds to reduce operations
         - Total cost less than 3000

            - a node can be passed through more than once to optimize cost  

         - later
            - first 20 paths
        """
        assert (from_vertex and to_vertex) in self._graph_dict.keys()

        queue = [[[from_vertex],0]]

        need_to_visit = set(self.getVertices())
        routes = []

        while queue: #queue not empty

            path,total_cost = queue.pop(0)
            visited = set(path)
            node = path[-1]

            neighbors = self.getNeighbors(node)

            diff = need_to_visit.symmetric_difference(visited) 
            # # mark as visted:
            # if node in need_to_visit:
            #     need_to_visit.pop(need_to_visit.index(node))

            for neighbor,cost in neighbors:
                
                new_path = list(path)
                new_cost = total_cost + cost
                # if needed check for repeat condition

                if neighbor in new_path:
                    continue

                new_path.append(neighbor)
                queue.append([new_path,cost])

                if neighbor == to_vertex:
                    routes.append([new_path,new_cost])

            if len(diff) < 13:
                print(diff)
                #print(routes)
                break

    @staticmethod
    def worker(graph_instance,to_vertex,need_visit,task_q,route_q):
        #[[path],cost]
        for path,total_cost in (task_q.get,"STOP"):
            
            visited = set(path)
            node = path[-1]

            neighbors = graph_instance.getNeighbors(node)

            diff = need_visit.symmetric_difference(visited)

            for neighbor,cost in neighbors:
                    
                new_path = list(path)
                new_cost = total_cost + cost
                # if needed check for repeat condition

                if neighbor in new_path:
                    continue

                new_path.append(neighbor)
                task_q.put([new_path,cost])

                if neighbor == to_vertex:
                    route_q.put([new_path,new_cost]) 

            if len(diff) < 13:
                task_q.put("STOP")
            

    def multiworker_search(self,from_vertex,to_vertex):
        
        assert (from_vertex and to_vertex) in self._graph_dict.keys()

        task_queue = Queue()
        route_queue = Queue()
        need_to_visit = self.getVertices()

        task_queue.put([[[from_vertex],0]])
        NUMBER_OF_PROCESSES = 1

        for i in range(NUMBER_OF_PROCESSES):
            Process(target=self.worker,args=(self,to_vertex,need_to_visit,task_queue,route_queue)).start()

        print(task_queue.qsize())





