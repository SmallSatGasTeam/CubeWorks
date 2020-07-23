GASPACS Software VII: The Tests
==
Opening Notes:
--
The testing method we use is called unit testing. This method tests every component in the individual files that can possibly be tested with multiple tests. It is easy, organized and efficient.

Testing:
--
Location: 
	Unit Tests: ../tests
	runTest.py: ../runTests.py

Functionality:
We have many files in our software designed for testing. We perform a unit test on every program we write no matter how small. All these unit tests can be run all at one time from runTests.py. This file will call and run all the tests in the tests folder (see Location). Each test will only return whether it passed or failed.
