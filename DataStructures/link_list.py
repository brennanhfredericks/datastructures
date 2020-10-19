import itertools
import copy
class Node:
    def __init__(self,value,nxt=None,prv=None):

        self.next_node = nxt
        self.prev_node = prv
        self.value = value

    def __repr__(self):
        return f"Node({self.value})"

    def __str__(self):
        return f"{self.value}"



class Circular_Linked_List:
    def __init__(self):
        self._head = None
        self._count = 0
        self._current_idx = None
        self._current_node = None

    @property
    def size(self):
        return self._count

    @property
    def current_node(self):
        return self._current_node

    def _get_position(self,index):
        
        if index < 0:
            # negative index
            pos = self._count + index + 1
            pos = max(0,pos)
        else:
            #postive index
            pos = min(self._count,index)

        return pos

    def get_node_at_index(self,index):
        
        if self._head is None:
            return 
        
        position = self._get_position(index)
        
        if position == 0:
            return self._head

        if index < 0:
            position -=1
       

        this_node = self._head
        i = itertools.count()
        while (idx := next(i)) != position: #stop at previous node
            this_node = this_node.next_node

        return this_node

    def add_node_at_index(self,data,index=-1): #defualt add at end
        
        # link list is empty, create head node
        if self._head is None:
            self._head = Node(data)

            self._head.prev_node = self._head
            self._head.next_node = self._head
            self._count +=1

            self._current_node = self._head
            return True # successfully added

        position = self._get_position(index)
   
        if position == 0: # insert at the beginning

            tmp_node = self._head

            self._head = Node(data)
            self._head.next_node = tmp_node
            self._head.prev_node = tmp_node.prev_node

            tmp_node.prev_node = self._head
            
            self._current_node = self._head
            self._count += 1
            return True

        

        elif position == self._count: # insert at the end
            if self._count < 2:
                new_node = Node(data)
                new_node.next_node = self._head
                new_node.prev_node = self._head

                self._head.next_node = new_node
                self._head.prev_node = new_node

                self._count +=1
                return True
            else:
                end_node = self._head.prev_node
                
                new_node = Node(data)

                new_node.prev_node = end_node
                new_node.next_node = self._head
                
                end_node.next_node = new_node
                self._head.prev_node = new_node

                self._count +=1
                return True

        else:
            #TODO use current node or self._head for quicker iterations
            this_node = self._head
            i = itertools.count()
            while (idx := next(i)) != position: #stop at previous node
                 this_node = this_node.next_node

            new_node = Node(data)

            prv_node = this_node.prev_node

            prv_node.next_node = new_node
            new_node.prev_node = prv_node

            new_node.next_node = this_node
            this_node.prev_node = new_node
      

            self._count +=1
            return True
        
    def remove_node_at_index(self,index):
        
        if self._head is None:
            return 

        position = self._get_position(index)
       
        if index < 0:
            position -=1

        if position == 0:

            new_head = self._head.next_node
            end_node = self._head.prev_node

            new_head.prev_node = end_node
            end_node.next_node = new_head

            self._head = new_head
            self._current_node = self._head
            self._count -=1
        else:

            this_node = self._head
            i = itertools.count()
            while (idx := next(i)) != position: #stop at previous node
                this_node = this_node.next_node

            prv_node = this_node.prev_node
            nxt_node = this_node.next_node

            prv_node.next_node = nxt_node
            nxt_node.prev_node = prv_node

            del this_node
            self._count -=1

        

    def next_node(self):
        self._current_node = self._current_node.next_node
        
    def previous_node(self):
        self._current_node = self._current_node.prev_node
      

class Singly_Linked_List:

    def __init__(self):
        self._head = None
        self._count = 0
   
    @property
    def size(self):
        return self._count

    def get_node_at_index(self,index):
        
        if self._head is None:
            return False # successfully added

        #find node insert position
        if index < 0:
            # negative index
            pos = self._count + index 
            pos = max(0,pos)
        else:
            #postive index
            pos = min(self._count,index)
            

        #print(pos, end=" ")


        this_node = self._head
        i = itertools.count()
        while (idx := next(i)) != pos: 
                this_node = this_node.next_node

        return this_node.value

    
    def add_node_at_index(self,index:int,data):
        """
            - negative number wrap around
            - if abs(negative number) larger than len of link list the index will be inserted at beginning
            - if positive number larger than len of link the index will be inserted at the end
        """
        
        # link list is empty, create head node
        if self._head is None:
            self._head = Node(data)
            self._count +=1

            return True # successfully added

        #find node insert position
        if index < 0:
            # negative index
            pos = self._count + index + 1
            pos = max(0,pos)
        else:
            #postive index
            pos = min(self._count,index)
            
        #print(pos, end=" ")

        #insert at start
        if pos ==0:
            tmp = self._head
            self._head = Node(data)
            self._head.next_node = tmp
            self._count += 1
            return True
        else:
            this_node = self._head
            i = itertools.count()
            while (idx := next(i)) != pos-1: #stop at previous node
                 this_node = this_node.next_node

            tmp = this_node.next_node
            this_node.next_node = Node(data)
            this_node.next_node.next_node=tmp
            self._count +=1
            return True

    def remove_node_at_index(self,index:int):
        if self._head is None:
            return False

        #find node insert position
        if index < 0:
            # negative index
            pos = self._count + index 
            pos = max(0,pos)
        else:
            #postive index
            pos = min(self._count,index)

        
        if pos ==0:
            self._head = self._head.next_node 
            self._count -= 1
            return True
        else:
            this_node = self._head
            i = itertools.count()
            while (idx := next(i)) != pos-1: #stop at previous node
                 this_node = this_node.next_node

            
            this_node.next_node = this_node.next_node.next_node
       
            self._count -=1
            return True

    def add_node(self,value):

        if self._head is None:
            self._head = Node(value)
            self._count += 1
        else :
            this_node = self._head
            while this_node.next_node is not None:
                this_node = this_node.next_node
            this_node.next_node = Node(value)
            self._count += 1

    def add_node_after(self,new_value,exist_value):
        if self._head is None:
            return

        this_node = self._head

        while this_node.value != exist_value:
            if this_node.next_node is not None:
                this_node = this_node.next_node
            else:
                this_node = None
                break
        

        if this_node is not None:
            tmp = this_node.next_node
            this_node.next_node = Node(new_value)
            this_node.next_node.next_node=tmp
            self._count += 1

    def remove_node_after(self,value):
        if self._head is None:
            return

        this_node = self._head

        while this_node.value != value:
            if this_node.next_node is not None:
                this_node = this_node.next_node
            else:
                this_node = None
                break
        

        if this_node is not None:
            if this_node.next_node is not None:
                this_node.next_node = this_node.next_node.next_node
            self._count -= 1
       
    def remove_node(self):
        if self._head is None:
            return
        
        if self._head.next_node is None:
            self._head = None
            self._count -= 1
        else:
            remember_node,this_node = self._head,self._head.next_node
      
            while this_node.next_node is not None:
                remember_node,this_node = this_node,this_node.next_node

            remember_node.next_node = None
            self._count -= 1
    
    def iterate(self):
        
        if  self._head is None:
            return
        

        #retval.append(self._head.value)
        print(self._head.value,end=" ")

        this_node = self._head

        while this_node.next_node is not None:
            this_node = this_node.next_node
            print(this_node.value,end=" ")
            
        print()
            




if __name__ == "__main__":
    #exit(test_singly_link_list_with_index())
    pass