class Stack(object):
    '''Stack a FIFO data storage structure.'''

    def __init__(self):
        '''Create a new Stack data type.'''
        self.stk_pointer = []

    def clear(self):
        '''Clear the stack.'''
        self.stk_pointer = []

    def push(self, item):
        '''Push item to the top of the stack.'''
        self.stk_pointer.append(item)

    def pop(self):
        '''Pop the top item off the stack.'''
        return self.stk_pointer.pop()
