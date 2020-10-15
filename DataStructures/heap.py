
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




class MaxHeap:

    def __init__(self):
        """
            create-heap: create an empty heap
            heapify: create a heap out of given array of elements
        """
        pass

    def peek(self):
        """
            find-max (or find-min): find a maximum item of a max-heap, or a minimum item of a min-heap, respectively (a.k.a. peek)
        """
        pass

    def push(self):
        """
            insert: adding a new key to the heap (a.k.a., push[4])
        """
        pass

    def pop(self):
        """
            extract-max (or extract-min): returns the node of maximum value from a max heap [or minimum value from a min heap] after removing it from the heap (a.k.a., pop[5])
        """
        pass

    def delete(self):
        """
            delete-max (or delete-min): removing the root node of a max heap (or min heap), respectively
        """
        pass

    def replace(self):
        """
            replace: pop root and push a new key. More efficient than pop followed by push, since only need to balance once, not twice, and appropriate for fixed-size heaps.[6]
        """
        pass

    def size(self):
        """
            size: return the number of items in the heap.
        """
        pass

    def is_empty(self):
        """
            is-empty: return true if the heap is empty, false otherwise.
        """
        pass

    def _sift_up(self):
        """
            sift-up: move a node up in the tree, as long as needed; used to restore heap condition after insertion. Called "sift" because node moves up the tree until it reaches the correct level, as in a sieve.
        """

    def _sift_down(self):
        """
            sift-down: move a node down in the tree, similar to sift-up; used to restore heap condition after deletion or replacement
        """