
from tree import Node # type: ignore 

"""
    - The heap is one maximally efficient implementation of an abstract data type called a priority queue, and in fact, priority queues are often referred to as "heaps"
    - in a max heap, for any given node C, if P is a parent node of C, then the key (the value) of P is greater than or equal to the key of C. 
    - In a min heap, the key of P is less than or equal to the key of C.[2] 
    - The node at the "top" of the heap (with no parents) is called the root node.
    - When a heap is a complete binary tree, it has a smallest possible height—a heap with N nodes and for each node a branches always has loga N height.


    implementation
        
        - Thus the children of the node at position n would be at positions 2n and 2n + 1 in a one-based array, or 2n + 1 and 2n + 2 in a zero-based array.
        - Computing the index of the parent node of n-th element is also straightforward. For one-based arrays the parent of element n is located at position n/2. 
          Similarly, for zero-based arrays, the parent is located at position (n-1)/2 (floored).
        - Balancing a heap is done by sift-up or sift-down operations (swapping elements which are out of order).
"""

"""
In a complete binary tree every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible. 
It can have between 1 and 2h nodes at the last level h.[18] An alternative definition is a perfect tree whose rightmost leaves (perhaps all) have been removed. 
Some authors use the term complete to refer instead to a perfect binary tree as defined below, in which case they call this type of tree (with a possibly not filled last level) an almost complete binary tree or nearly complete binary tree.
[19][20] A complete binary tree can be efficiently represented using an array.[18]
"""

class _Heap:
    def __init__(self,items=[]):
        """
            create-heap: create an empty heap
            heapify: create a heap out of given array of elements
        """
        self._heap = [0] # to start at index

        for item in items:
            self._heap.append(item)
            self._shift_up(len(self._heap)-1)

    def peek(self):
        """
            find-max (or find-min): find a maximum item of a max-heap, or a minimum item of a min-heap, respectively (a.k.a. peek)
        """
        if len(self._heap) > 2: # check if any items are in the heap
            return self._heap[1]
        else:
            return False

    def push(self,data):
        """
            insert: adding a new key to the heap (a.k.a., push[4])
        """
        self._heap.append(data)
        self._shift_up(len(self._heap)-1)

    
    def pop(self):
        """
            extract-max (or extract-min): returns the node of maximum value from a max heap [or minimum value from a min heap] after removing it from the heap (a.k.a., pop[5])
        """
        if len(self._heap) > 2: # need to ensure property of heap is kept aft top item is report moved
            self._swap(1,len(self._heap)-1) #swap first and last element
            maxvalue = self._heap.pop() # last item in the list
            self._shift_down(1) #top element
        elif len(self._heap) == 2:
            maxvalue = self._heap.pop() #last item in the list
        else:
            maxvalue = False # heap empty

        return False


    def _swap(self,i,j):
        self._heap[i],self._heap[j] = self._heap[j],self._heap[i]

    

    def delete(self):
        """
            delete-max (or delete-min): removing the root node of a max heap (or min heap), respectively
        """
        if len(self._heap) >2:
            self.pop()
            return True
        else:
            return False

    def replace(self,data):
        """
            replace: pop root and push a new key. More efficient than pop followed by push, since only need to balance once, not twice, and appropriate for fixed-size heaps.[6]
        """
        if len(self._heap) >2:
             retval = self.pop()
             self.push(data)

             return retval
        else:
            return False

    def size(self):
        """
            size: return the number of items in the heap.
        """
        return len(self._heap)-1

    def is_empty(self):
        """
            is-empty: return true if the heap is empty, false otherwise.
        """
        if len(self._heap)<2:
            return True
        else:
            return False

class MaxHeap(_Heap):

    def _shift_up(self,idx):
        """
           
            Computing the index of the parent node of n-th element is also straightforward. For one-based arrays the parent of element n is located at position n/2
            sift-up: move a node up in the tree, as long as needed; used to restore heap condition after insertion. Called "sift" because node moves up the tree until it reaches the correct level, as in a sieve.
        """
        parent = idx//2
        if idx <=1: # heep has only one item , no shift needed
            return
        elif self._heap[parent] < self._heap[idx]:
            self._swap(parent,idx)
            self._shift_up(parent)
        
    def _shift_down(self,idx):
        """
            Thus the children of the node at position n would be at positions 2n and 2n + 1 in a one-based array
            sift-down: move a node down in the tree, similar to sift-up; used to restore heap condition after deletion or replacement
        """
        left_child = 2*idx
        right_child=2*idx + 1


        lowest_key = idx

        if len(self._heap) > left_child and self._heap[lowest_key] < self._heap[left_child]:
            lowest_key = left_child

        if len(self._heap) > right_child and self._heap[lowest_key] < self._heap[right_child]:
            lowest_key = right_child

        if idx != lowest_key:
            self._swap(idx,lowest_key)
            self._shift_down(lowest_key)

class MinHeap(_Heap):
    
    def _shift_up(self,idx):
        """
           
            Computing the index of the parent node of n-th element is also straightforward. For one-based arrays the parent of element n is located at position n/2
            sift-up: move a node up in the tree, as long as needed; used to restore heap condition after insertion. Called "sift" because node moves up the tree until it reaches the correct level, as in a sieve.
        """
        parent = idx//2
        if idx <=1: # heep has only one item , no shift needed
            return
        elif self._heap[parent] > self._heap[idx]:
            self._swap(parent,idx)
            self._shift_up(parent)
        
    def _shift_down(self,idx):
        """
            Thus the children of the node at position n would be at positions 2n and 2n + 1 in a one-based array
            sift-down: move a node down in the tree, similar to sift-up; used to restore heap condition after deletion or replacement
        """
        left_child = 2*idx
        right_child=2*idx + 1


        lowest_key = idx

        if len(self._heap) > left_child and self._heap[lowest_key] > self._heap[left_child]:
            lowest_key = left_child

        if len(self._heap) > right_child and self._heap[lowest_key] > self._heap[right_child]:
            lowest_key = right_child

        if idx != lowest_key:
            self._swap(idx,lowest_key)
            self._shift_down(lowest_key)

def debug_maxheap(items):
    maxheap = MaxHeap(items=items)

    # print(maxheap.size())
    # print(maxheap.is_empty())
    print(maxheap.peek())
    maxheap.push(100)
    maxheap.push(100)
    print(maxheap.peek())
    maxheap.delete()
    print(maxheap.peek())
    maxheap.replace(150)
    print(maxheap.peek())
    maxheap.pop()
    print(maxheap.peek())

def debug_minheap(items):
    minheap = MinHeap(items=items)

    print(minheap.peek())
    minheap.push(100)
    minheap.push(100)
    print(minheap.peek())
    minheap.delete()
    print(minheap.peek())
    minheap.replace(150)
    print(minheap.peek())
    minheap.pop()
    print(minheap.peek())




if __name__ == "__main__":
    items = [200,5,12,32,1,2,78,4,8]

    debug_maxheap(items)

    debug_minheap(items)

