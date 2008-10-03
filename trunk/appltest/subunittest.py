import unittest, inspect

class TestCase(unittest.TestCase):
    def __filter(self, object):
        return inspect.ismethod(object) and object.__name__.startswith('subtest')
    
    def _execsubtests(self):
        subtests = inspect.getmembers(self, self.__filter)
        for subtest in subtests:
            subtest[1]()


class TestLoader(unittest.TestLoader):
    def __init__(self):
        self.suiteClass = self.__getSuiteClass

    def __getSuiteClass(self, testlist):
        return TestSuite(testlist)
        

class TestSuite(unittest.TestSuite):
    def run(self, result):
        if 'setUpSuite' in dir(self) and inspect.ismethod(self.setUpSuite):
            self.setUpSuite()
        unittest.TestSuite.run(self, result)
        if 'tearDownSuite' in dir(self) and inspect.ismethod(self.tearDownSuite):
            self.tearDownSuite()
