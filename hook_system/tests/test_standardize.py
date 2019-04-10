import unittest
from processor.Src.standardize import *

class TestStandardize(unittest.TestCase):

    def test_replace(self):
        '''
        Test that the replaceIfContiains function replaces strings as specified
        '''
        result = replaceIfContains("test", "this is just a test", "unittest")
        self.assertEqual(result, "this is just a unnittest")


