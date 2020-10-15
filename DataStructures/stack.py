from collections import deque

#LIFO -> Last In First Out -> Thread safe
class LIFO_Deque_Stack:

    def __init__(self,stack=list(),max_size=5):
        self._stack = deque(stack,maxlen=max_size)

    def push(self,data):

        try:
            self._stack.append(data)
            return True
  
        except Exception as e:
            return False

    def pop(self):
        if len(self._stack) > 0:
            return self._stack.pop() # by default returns last item
        else:
            return None

    def peek(self):    
        if len(self._stack) >  0:
            return self._stack[-1]
        else:
            return None

    def size(self):
        return len(self._stack)

    def __repr__(self):
        return self._stack.__repr__()
    
    def __str__(self):
        return self._stack.__str__()

#FIFO -> First In First Out -> Thread safe
class FIFO_Deque_Stack:

    def __init__(self,stack=list(),max_size=5):
        self._stack = deque(stack,maxlen=max_size)
 

    def push(self,data):

        try:
            self._stack.append(data)
            return True
  
        except Exception as e:
            return False

    def pop(self):
        if len(self._stack) > 0:
            return self._stack.popleft() # by default returns last item
        else:
            return None

    def peek(self):    
        if len(self._stack) >  0:
            return self._stack[0]
        else:
            return None

    def size(self):
        return len(self._stack)

    def __repr__(self):
        return self._stack.__repr__()
    
    def __str__(self):
        return self._stack.__str__()

#LIFO -> Last In First Out
class LIFO_List_Stack:

    def __init__(self,stack=list(),max_size=5):
        self._stack = stack
        self._max_size = max_size

    def push(self,data):

        try:
            if len(self._stack) == self._max_size:
                self._stack.pop(0)
                
            self._stack.append(data)
            return True
  
        except Exception as e:
            return False

    def pop(self):
        if len(self._stack) > 0:
            return self._stack.pop() # by default returns last item
        else:
            return None

    def peek(self):    
        if len(self._stack) >  0:
            return self._stack[-1]
        else:
            return None

    def size(self):
        return len(self._stack)

    def __repr__(self):
        return self._stack.__repr__()
    
    def __str__(self):
        return self._stack.__str__()

#FIFO -> First In First Out
class FIFO_List_Stack:

    def __init__(self,stack=list(),max_size=5):
        self._stack = stack
        self._max_size = max_size

    def push(self,data):

        try:
            if len(self._stack) == self._max_size:
                self._stack.pop(0)
                
            self._stack.append(data)
            return True
  
        except Exception as e:
            return False

    def pop(self):
        if len(self._stack) > 0:
            return self._stack.pop(0) # by default returns last item
        else:
            return None

    def peek(self):    
        if len(self._stack) >  0:
            return self._stack[0]
        else:
            return None

    def size(self):
        return len(self._stack)

    def __repr__(self):
        return self._stack.__repr__()
    
    def __str__(self):
        return self._stack.__str__()


def test_fifo_deque_stack():
    mystack = FIFO_Deque_Stack(stack=[101,100],max_size=5)
    mystack.push(99)
    mystack.push(88)
    mystack.push(77)
    print(mystack)
    print(mystack.size())
    mystack.push(66)
    mystack.push(55)
    mystack.push(44)
    mystack.push(33)
    print(mystack)
    
    #assert  mystack.peek() == 44
    mystack.pop()
    print(mystack)
    assert mystack.push(99)
    print(mystack)

    print(mystack.size())
    # print(mystack.peek())

def test_lifo_deque_stack():
    mystack = LIFO_Deque_Stack(stack=[101,100],max_size=5)
    mystack.push(99)
    mystack.push(88)
    mystack.push(77)
    print(mystack)
    print(mystack.size())
    mystack.push(66)
    mystack.push(55)
    mystack.push(44)
    
    print(mystack)
    
    assert  mystack.peek() == 44
    mystack.pop()
    print(mystack)
    assert mystack.push(99)
    print(mystack)

    print(mystack.size())
    # print(mystack.peek())

def test_lifo_stack():
    mystack = LIFO_List_Stack(max_size=5)
    mystack.push(99)
    mystack.push(88)
    mystack.push(77)
    mystack.push(66)
    mystack.push(55)
    mystack.push(44)
    
    print(mystack)
    
    assert  mystack.peek() == 44
    mystack.pop()
    print(mystack)
    assert mystack.push(99)
    print(mystack)

    print(mystack.size())
    # print(mystack.peek())
    
def test_fifo_stack():
    mystack = FIFO_List_Stack(max_size=2)
    mystack.push(99)
    mystack.push(88)
    mystack.push(77)
    mystack.push(66)
    mystack.push(55)
    mystack.push(44)
    
    print(mystack)
    
    #assert  mystack.peek() == 88
    mystack.pop()
    print(mystack)
    assert mystack.push(99)
    print(mystack)

    print(mystack.size())
    # print(mystack.peek())


if __name__ == "__main__":
    test_fifo_deque_stack()
    #test_lifo_deque_stack()
    #test_fifo_stack()
    #exit(test_lifo_stack())
