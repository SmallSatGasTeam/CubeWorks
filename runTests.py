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
