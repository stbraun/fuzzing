# coding=utf-8
"""
Copyright (c) 2015 Stefan Braun

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import unittest

from fuzzing.fuzzer import TestStatCounter, Status


class TestStatCounterTests(unittest.TestCase):
    """Test cases for test result class."""

    def test_create_empty_instance(self):
        """Create instance of status counter without keys_."""
        tsc = TestStatCounter([])
        self.assertIsNotNone(tsc, msg='Instance created.')

    def test_create_instance(self):
        """Create instance of status counter."""
        tsc = TestStatCounter(['a', 'b'])
        self.assertIsNotNone(tsc, msg='Instance created.')

    def test_add_new_test_result(self):
        """Add new test result and check update of stats."""
        key = 'aaa'
        status = Status.SUCCESS
        tsc = TestStatCounter([key])
        self.assertEqual(0, tsc.retrieve_count(key, status),
                         msg='Counter is zero yet.')
        tsc.add(key=key, status=status)
        self.assertEqual(1, tsc.retrieve_count(key, status),
                         msg='Counter is incremented once.')
        tsc.add(key=key, status=status)
        tsc.add(key=key, status=status)
        self.assertEqual(3, tsc.retrieve_count(key, status),
                         msg='Counter is incremented twice.')

    def test_cumulated_count(self):
        """Retrieve the cumulated count for the instance."""
        keys = ['a', 'b', 'c']
        counts = [2, 3, 4, 5, 6, 7]
        expected = sum(counts)
        tsc = TestStatCounter(keys=keys)
        self.assertEqual(0, tsc.cumulated_counts())
        self.__increment_counter(tsc, keys, counts)
        self.assertEqual(expected, tsc.cumulated_counts())

    def test_cumulated_count_for_status(self):
        """Retrieve the cumulated count for given status."""
        keys = ['a', 'b', 'c']
        counts = [2, 3, 4, 5, 6, 7]
        expected = sum([x for x in counts if x % 2 == 1])
        tsc = TestStatCounter(keys=keys)
        self.assertEqual(0, tsc.cumulated_counts_for_status(Status.SUCCESS))
        self.__increment_counter(tsc, keys, counts)
        self.assertEqual(expected,
                         tsc.cumulated_counts_for_status(Status.SUCCESS))

    def test_merge_matching_keys(self):
        """Merge two test statistics.
        Both have same set of keys_.
        """
        keys = ['a', 'b', 'c']
        counts_1 = [2, 3, 4, 5, 6, 7]
        counts_2 = [3, 4, 5, 6, 7, 8]
        tsc_1 = TestStatCounter(keys=keys)
        self.__increment_counter(tsc_1, keys, counts_1)
        tsc_2 = TestStatCounter(keys=keys)
        self.__increment_counter(tsc_2, keys, counts_2)
        tsc = tsc_1 + tsc_2
        self.assertEqual(tsc.cumulated_counts(),
                         tsc_1.cumulated_counts() + tsc_2.cumulated_counts())

    def test_merge_differing_keys(self):
        """Merge two test statistics.
        The statistics have different sets of keys_.
        """
        keys_1 = ['a', 'b', 'c']
        keys_2 = ['b', 'c', 'd']
        counts_1 = [2, 3, 4, 5, 6, 7]
        counts_2 = [3, 4, 5, 6, 7, 8]
        tsc_1 = TestStatCounter(keys=keys_1)
        self.__increment_counter(tsc_1, keys_1, counts_1)
        tsc_2 = TestStatCounter(keys=keys_2)
        self.__increment_counter(tsc_2, keys_2, counts_2)
        tsc = tsc_1 + tsc_2
        self.assertEqual(tsc.cumulated_counts(),
                         tsc_1.cumulated_counts() + tsc_2.cumulated_counts())

    def test_retrieve_count(self):
        """Retrieve count for specified key and status."""
        keys = ['a', 'b']
        counts = [2, 3, 4, 5]
        tsc = TestStatCounter(keys)
        self.__increment_counter(tsc, keys, counts)
        self.assertEqual(counts[0],
                         tsc.retrieve_count(keys[0], Status.FAILED))
        self.assertEqual(counts[1],
                         tsc.retrieve_count(keys[0], Status.SUCCESS))

    def __increment_counter(self, tsc, keys, counts):
        """Increment counters for each key/status pair.

        Iterate over keys_ / status / counts and increment the counters.

        :param tsc: the unit under test.
        :param keys: list of keys_
        :param counts: list of counts to set.
        """
        print('Status: {}'.format(Status))
        assert len(keys) * 2 <= len(counts)
        for i, key in enumerate(keys):
            for _ in range(counts[2 * i]):
                tsc.add(key, Status.FAILED)
            for _ in range(counts[2 * i + 1]):
                tsc.add(key, Status.SUCCESS)
