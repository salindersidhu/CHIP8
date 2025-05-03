import unittest
from chip8.stack import Stack

class TestStack(unittest.TestCase):
    def test_push_and_pop(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        self.assertFalse(stack.isEmpty())
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.isEmpty())

    def test_clear(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.clear()
        self.assertTrue(stack.isEmpty())

    def test_pop_empty_raises(self):
        stack = Stack()
        with self.assertRaises(Exception) as context:
            stack.pop()
        self.assertIn('Cannot pop from empty stack', str(context.exception))
