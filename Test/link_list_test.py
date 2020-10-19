
import sys

sys.path.insert(0,'e:\\python\\data_structures_algorithms\\DataStructures')


from link_list import Singly_Linked_List, Circular_Linked_List # type: ignore

def test_singly_link_list():
    singlylinklist = Singly_Linked_List()
    [singlylinklist.add_node(n) for n in range(2)]
    
    #singlylinklist.iterate()
    singlylinklist.add_node_after(5,0)
    # print(singlylinklist.size)
    assert singlylinklist.size == 3

    singlylinklist.remove_node()
    assert singlylinklist.size == 2
    #singlylinklist.iterate()
    singlylinklist.add_node(1)
    singlylinklist.add_node(2)
    assert singlylinklist.size == 4
    #singlylinklist.iterate()
    singlylinklist.add_node_after(7,1)
    singlylinklist.add_node_after(10,0)
    singlylinklist.add_node_after(15,2)
    assert singlylinklist.size == 7
    #singlylinklist.iterate()

    #singlylinklist.remove_node_after(5)
    #singlylinklist.iterate()
    singlylinklist.remove_node_after(15)
    singlylinklist.remove_node_after(0)
    assert singlylinklist.size == 5
    #singlylinklist.iterate()

def test_singly_link_list_with_index():
    sll = Singly_Linked_List()

    sll.add_node_at_index(0,'a')
    sll.add_node_at_index(2,'b')
    sll.add_node_at_index(1,'c')
    sll.add_node_at_index(0,'d')
    sll.add_node_at_index(-1,'e')
    sll.add_node_at_index(-4,'f')
    sll.add_node_at_index(-2,'g')
    sll.add_node_at_index(-1,'h')

    
    #sll.iterate()
    assert sll.get_node_at_index(0) == 'd'
    assert sll.get_node_at_index(-2) == 'e'
    assert sll.get_node_at_index(-1) == 'h'

    t = sll.get_node_at_index(1)
    sll.remove_node_at_index(0)
    assert sll.get_node_at_index(0) == t
    sll.remove_node_at_index(4)
    sll.remove_node_at_index(-1)
    #sll.iterate()
    #print(sll.size)


def test_cicular_link_list():
    cll = Circular_Linked_List()


    
    cll.add_node_at_index('B')
    cll.add_node_at_index('C')
    cll.add_node_at_index('D')
    cll.add_node_at_index('E')
    cll.add_node_at_index('A',index=0)
    cll.add_node_at_index('F')
    cll.add_node_at_index('@',index=1)

    # cll.add_node_at_index('C',2)
    # cll.add_node_at_index('D',3)
    # cll.add_node_at_index('E',4)
    # cll.add_node_at_index('F',5)
    


    for _ in range(20):
        print(cll.current_node , end=" ")
        cll.next_node()
    print()
    for _ in range(20):
        print(cll.current_node , end=" ")
        cll.previous_node()

test_singly_link_list()
test_singly_link_list_with_index()

test_cicular_link_list()
