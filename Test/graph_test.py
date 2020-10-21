
import sys

sys.path.insert(0, 'e:\\python\\data_structures_algorithms\\DataStructures')
from graph import Graph  # type: ignore

def test_graph():

    elements = {"a": ["b","b", "c"],
                "b": ["a", "d"],
                "c": ["a", "d"],
                "d": ["e"],
                "e": ["d"]
                }

    mygraph = Graph(elements)

    #mygraph.viewGraph()

    #print(mygraph.getVertices())
    mygraph.addVertice('f')
    #print(mygraph.getVertices())
    

    mygraph.addEdge('a','f')
    mygraph.addEdge('f','a')
    mygraph.addEdge('f','b')
    #mygraph.viewGraph()
    print(mygraph.adjacent('a','f'))
    print(mygraph.adjacent('f','a'))
    print(mygraph.adjacent('f','c'))

    print(mygraph.neighbors('c'))

    mygraph.remove_vertex('f')
    mygraph.viewGraph()
    mygraph.remove_edge('a','b')
    mygraph.viewGraph()

def test_graph1():
    """

    A - B - C - D
    |       |
    K - M   E - F 
    |   |   |
    L   N - G - J 
        |   |
        O - H - I   
    """
    elements = {
        "A": ["B","K"],
        "B": ["C","A"],
        "C": ["B","D","E"],
        "D": ["C"],
        "E": ["C","F","G"],
        "F": ["E"],
        "G": ["E","J","H","N"],
        "H": ["G","I","O"],
        "I": ["H"],
        "J": ["G"],
        "K": ["A","L","M"],
        "L": ["K"],
        "M": ["K","N"],
        "N": ["M","G","O"],
        "O": ["N","H"]
    }
    mygraph = Graph(elements)
    # print(mygraph.neighbors('K'))
    # print(mygraph.neighbors('C'))
    # print(mygraph.neighbors('G'))

    #print(mygraph.all_paths('A','I'))
    # print(mygraph.shortest_path('A','O'))
    # print(mygraph.longest_path('A','O'))

    #print(mygraph.all_destinations('A'))

    #print(mygraph.furthest_path('A'))
    print(mygraph.deadend_paths('I'))
#test_graph()
test_graph1()


