import unittest
import flask_testing

from test_api import TestAPI


def hook_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestAPI))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(hook_suite())

