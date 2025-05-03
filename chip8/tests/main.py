import unittest
import os

if __name__ == '__main__':
    # Discover and run all tests in files starting with test_ in the current directory
    test_dir = os.path.dirname(__file__)
    suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')
    unittest.TextTestRunner(verbosity=1).run(suite)
