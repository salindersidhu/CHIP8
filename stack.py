class Stack(object):
    '''Stack a FIFO data storage structure.'''

    def __init__(self):
        '''Create a new Stack data type.'''
        # Exceptions
        self.__emptyStackException = Exception('Cannot pop from empty stack!')
        # Create an empty list to store stack content
        self.__stk_pointer = []

    def clear(self):
        '''Clear the stack.'''
        self.__stk_pointer = []

    def push(self, item):
        '''Push item to the top of the stack.'''
        self.__stk_pointer.append(item)

    def pop(self):
        '''Pop the top item off the stack.'''
        try:
            return self.__stk_pointer.pop()
        except IndexError:
            raise self.__emptyStackException
