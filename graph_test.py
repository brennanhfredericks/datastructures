
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

test_graph()


