# coding=utf-8
"""
Copyright (c) 2015 Stefan Braun

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import unittest
from collections import Counter

from fuzzing.fuzzer import TestStatCounter


class TestStatCounterTests(unittest.TestCase):
    """Test cases for test result class."""

    def test_create_empty_instance(self):
        """Create instance of status counter without keys."""
        tsc = TestStatCounter([])
        self.assertIsNotNone(tsc, msg='Instance created.')

    def test_create_instance(self):
        """Create instance of status counter."""
        tsc = TestStatCounter(['a', 'b'])
        self.assertIsNotNone(tsc, msg='Instance created.')

    def test_stats_structure(self):
        """Test the structure returning test statistics."""
        keys = ['key_1', 'key_2']
        tsc = TestStatCounter(keys)
        self.assertIsNotNone(tsc, msg='Instance created.')
        stats = tsc.stats()
        self.assertIsInstance(stats, dict, msg='Is dictionary')
        self.assertSetEqual(set(keys), set(stats.keys()), msg='Keys matching.')
        for val in stats.values():
            self.assertIsInstance(val, Counter, 'Counter expected.')

    def test_add_new_test_result(self):
        """Add new test result and check update of stats."""
        key = 'aaa'
        status = 'ok'
        tsc = TestStatCounter([key])
        self.assertEqual(0, tsc.stats()[key][status], msg='Counter is zero yet.')
        tsc.add(key=key, status=status)
        self.assertEqual(1, tsc.stats()[key][status], msg='Counter is incremented once.')
        tsc.add(key=key, status=status)
        tsc.add(key=key, status=status)
        self.assertEqual(3, tsc.stats()[key][status], msg='Counter is incremented twice.')

    def test_cumulated_count(self):
        """Retrieve the cumulated count for the instance."""
        keys = ['a', 'b', 'c']
        status = ['s1', 's2']
        counts = [2, 3, 4, 5, 6, 7]
        expected = sum(counts)
        tsc = TestStatCounter(keys=keys)
        self.assertEqual(0, tsc.cumulated_counts())
        self.__increment_counter(tsc, keys, status, counts)
        self.assertEqual(expected, tsc.cumulated_counts())

    def test_cumulated_count_for_status(self):
        """Retrieve the cumulated count for given status."""
        keys = ['a', 'b', 'c']
        status = ['s1', 's2']
        counts = [2, 3, 4, 5, 6, 7]
        expected = sum([x for x in counts if x % 2 == 0])
        tsc = TestStatCounter(keys=keys)
        self.assertEqual(0, tsc.cumulated_counts_for_status('s1'))
        self.__increment_counter(tsc, keys, status, counts)
        self.assertEqual(expected, tsc.cumulated_counts_for_status('s1'))

    def __increment_counter(self, tsc, keys, status, counts):
        """Increment counters for each key/status pair.

        Iterate over keys / status / counts and increment the counters.

        :param tsc: the unit under test.
        :param keys: list of keys
        :param status: list of status
        :param counts: list of counts to set.
        """
        assert len(keys)*len(status) <= len(counts)
        for i, key in enumerate(keys):
            for j, stat in enumerate(status):
                for _ in range(counts[i*len(status) + j]):
                    tsc.add(key, stat)
