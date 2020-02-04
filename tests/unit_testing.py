import unittest

def divByTwo(param):
    return param / 2

class DemoTest(unittest.TestCase):
    def testDivTwo(self):
        # (what we want to test, expected output)
        self.assertEqual(divByTwo(4), 2)
    def testtewo(self):
        self.assertEqual(divByTwo(4), 3)
    def testtree(self):
        self.assertEqual(divByTwo(4), 2)
    
if __name__ == '__main__':
    unittest.main()
