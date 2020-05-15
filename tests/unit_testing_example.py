import unittest

def divByTwo(param):
    return param / 2

class DemoTest(unittest.TestCase):
    """
    A test case containing sets of assertions in the form of class methods.
    """
    def testDivTwo(self):
        """Asserts that 4 / 2 == 2.  Assertion should pass"""
        self.assertEqual(divByTwo(4), 2)
    def testtewo(self):
        """Asserts that 4 / 2 == 3.  Assertion should fail"""
        self.assertEqual(divByTwo(4), 3)
    def testhree(self):
        """Asserts that 6 / 2 == 3.  Assertion should pass"""
        self.assertEqual(divByTwo(6), 3)
    def testtree(self):
        """Asserts that 'tree' / 2 == 3.  Assertion should result in an error"""
        self.assertEqual(divByTwo('tree'), 3)

    
if __name__ == '__main__':
    unittest.main()
