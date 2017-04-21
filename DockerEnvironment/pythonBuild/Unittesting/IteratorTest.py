import unittest
from DockerEnvironment.pythonBuild.Iterator.HandlerIterator import myIterator

class IteratorTest(unittest.TestCase):

    def test_iteration(self):
        handler_list_example = ['#1', '#2', '#3']
        #create handler iterator
        iterator = myIterator(handler_list_example)
        counter = 0
        for handle in iterator:
            self.assertEqual(handler_list_example[counter],handle)
            counter += 1

if __name__ == '__main__':
    unittest.main()