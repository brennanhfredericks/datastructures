
from collections import defaultdict


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

        queue = [[[from_vertex],0]]

        
        routes = []

        if from_vertex == to_vertex:
            print("From and To node are the same")
            return

        while queue:
            #print(len(queue))
            path,total_cost = queue.pop(0)
            node = path[-1]

            neighbors = self.getNeighbors(node)

            for neighbor,cost in neighbors:
     
                new_path = list(path)
                new_cost = total_cost + cost
                if neighbor in new_path or new_cost > cost_bound:
                    continue

                new_path.append(neighbor)
                queue.append([new_path,new_cost])

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

        

