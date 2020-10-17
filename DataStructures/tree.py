import random

#Here is my simple recursive implementation of binary search tree.

class Node:

    def __init__(self,val):
        self.left_child = None
        self.right_child = None
        self.value = val

    def __repr__(self):
        return f"Node({self.value})"

    def __str__(self):
        return f"{self.value}"


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def getRoot(self):
        return self.root
    
    def add(self,val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self,val,node):
      
        if val < node.value:
            if node.left_child is not None:
                self._add(val,node.left_child)
            else:
                node.left_child = Node(val)
        else:
    
            if node.right_child is not None:
                self._add(val,node.right_child)
            else:
                node.right_child = Node(val)

    def find(self,val):
        if self.root is not None:
            return self._find(val,self.root)
        else:
            return None

    
    def _find(self,val,node):
        if val == node.value:
            return node
        elif (val < node.value and node.left_child is not None):
            return self._find(val,node.left_child)
        elif (val > node.value and node.right_child is not None):
            return self._find(val,node.right_child)
        else:
            #node not found
            return None

 
    
    def deleteTree(self):
        self.root = None
    
    def printTree(self):
        if self.root is not None:
            self._printTree(self.root)
        
       

    def _printTree(self,node):
        if node is not None:
            self._printTree(node.left_child)
            print(str(node.value) + ' ')
            self._printTree(node.right_child)
        


if __name__ == "__main__":

    tree = BinarySearchTree()

    init_tree = (tree.add(val) for val  in [5,10,1,8])

    while True:
        
        try:
            next(init_tree)
        except:
            break
    
    #tree.printTree()

    print(tree.find(9))
