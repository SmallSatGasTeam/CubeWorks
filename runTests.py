<<<<<<< HEAD
import unittest

from tests import unit_testing_example

def run():
    """
    Defines a suite of unit tests from the tests module and runs them.  
    """
    suite = unittest.TestSuite()

    tests = [unit_testing_example.DemoTest]

    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    runner = unittest.TextTestRunner(verbosity=2)
    print(runner.run(suite))


if __name__ == '__main__':
    run()
=======
import unittest

from tests import unit_testing_example, testCamera

def run():
    """
    Defines a suite of unit tests from the tests module and runs them.  
    """
    suite = unittest.TestSuite()

    tests = [unit_testing_example.DemoTest, testCamera.TestCamera]

    for test in tests:
        suite.addTest(unittest.makeSuite(test))

    runner = unittest.TextTestRunner(verbosity=2)
    print(runner.run(suite))


if __name__ == '__main__':
    run()
>>>>>>> 143542699d5e03c2eb520f08e62d1eda6122dc4f
