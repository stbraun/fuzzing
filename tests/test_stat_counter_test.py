# coding=utf-8
"""Test cases for test result class."""
# Copyright (c) 2015-2018 Stefan Braun
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


from fuzzing.fuzzer import TestStatCounter, Status


def test_create_empty_instance():
    """Create instance of status counter without keys_."""
    tsc = TestStatCounter([])
    assert tsc is not None, 'Instance created.'


def test_create_instance():
    """Create instance of status counter."""
    tsc = TestStatCounter(['a', 'b'])
    assert tsc is not None, 'Instance created.'


def test_add_new_test_result():
    """Add new test result and check update of stats."""
    key = 'aaa'
    status = Status.SUCCESS
    tsc = TestStatCounter([key])
    assert tsc.retrieve_count(key, status) == 0, 'Counter is zero yet.'
    tsc.add(key=key, status=status)
    assert tsc.retrieve_count(key, status) == 1
    tsc.add(key=key, status=status)
    tsc.add(key=key, status=status)
    assert tsc.retrieve_count(key, status) == 3


def test_cumulated_count():
    """Retrieve the cumulated count for the instance."""
    keys = ['a', 'b', 'c']
    counts = [2, 3, 4, 5, 6, 7]
    expected = sum(counts)
    tsc = TestStatCounter(keys=keys)
    assert tsc.cumulated_counts() == 0
    __increment_counter(tsc, keys, counts)
    assert tsc.cumulated_counts() == expected


def test_cumulated_count_for_status():
    """Retrieve the cumulated count for given status."""
    keys = ['a', 'b', 'c']
    counts = [2, 3, 4, 5, 6, 7]
    expected = sum([x for x in counts if x % 2 == 1])
    tsc = TestStatCounter(keys=keys)
    assert tsc.cumulated_counts_for_status(Status.SUCCESS) == 0
    __increment_counter(tsc, keys, counts)
    actual = tsc.cumulated_counts_for_status(Status.SUCCESS)
    assert actual == expected


def test_merge_matching_keys():
    """Merge two test statistics.

    Both have same set of keys_.
    """
    keys = ['a', 'b', 'c']
    counts_1 = [2, 3, 4, 5, 6, 7]
    counts_2 = [3, 4, 5, 6, 7, 8]
    tsc_1 = TestStatCounter(keys=keys)
    __increment_counter(tsc_1, keys, counts_1)
    tsc_2 = TestStatCounter(keys=keys)
    __increment_counter(tsc_2, keys, counts_2)
    tsc = tsc_1 + tsc_2
    expected = tsc.cumulated_counts()
    actual = tsc_1.cumulated_counts() + tsc_2.cumulated_counts()
    assert actual == expected


def test_merge_differing_keys():
    """Merge two test statistics.

    The statistics have different sets of keys_.
    """
    keys_1 = ['a', 'b', 'c']
    keys_2 = ['b', 'c', 'd']
    counts_1 = [2, 3, 4, 5, 6, 7]
    counts_2 = [3, 4, 5, 6, 7, 8]
    tsc_1 = TestStatCounter(keys=keys_1)
    __increment_counter(tsc_1, keys_1, counts_1)
    tsc_2 = TestStatCounter(keys=keys_2)
    __increment_counter(tsc_2, keys_2, counts_2)
    tsc = tsc_1 + tsc_2
    expected = tsc.cumulated_counts()
    actual = tsc_1.cumulated_counts() + tsc_2.cumulated_counts()
    assert actual == expected


def test_retrieve_count():
    """Retrieve count for specified key and status."""
    keys = ['a', 'b']
    counts = [2, 3, 4, 5]
    tsc = TestStatCounter(keys)
    __increment_counter(tsc, keys, counts)
    assert counts[0] == tsc.retrieve_count(keys[0], Status.FAILED)
    assert counts[1] == tsc.retrieve_count(keys[0], Status.SUCCESS)


def __increment_counter(tsc, keys, counts):
    """Increment counters for each key/status pair.

    Iterate over keys_ / status / counts and increment the counters.

    :param tsc: the unit under test.
    :param keys: list of keys_
    :param counts: list of counts to set.
    """
    assert len(keys) * 2 <= len(counts)
    for i, key in enumerate(keys):
        for _ in range(counts[2 * i]):
            tsc.add(key, Status.FAILED)
        for _ in range(counts[2 * i + 1]):
            tsc.add(key, Status.SUCCESS)
