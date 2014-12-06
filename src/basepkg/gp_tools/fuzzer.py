# coding=utf-8
"""Fuzz testing module.

A toolbox to create fuzzers for random testing of software.
"""

import random
import math
from copy import deepcopy

seed_content = """A boring multiline string.
Just for demonstration; makes no sense at all.
"""


def fuzz_string(seed_str, rounds=100, fuzz_factor=50):
    """A random fuzzer for a simulated text viewer application.

    :param seed_str: the string to use as seed for fuzzing.
    :param rounds: number of fuzzed variants to supply.
    :param fuzz_factor: degree of fuzzing = 1 / fuzz_factor
    :return: list of fuzzed variants of seed_str.
    :rtype: [str]
    """
    buf = bytearray(seed_str, encoding="utf8")
    variants = []
    for _ in range(rounds):
        fuzzed = fuzzer(buf, fuzz_factor)
        variants.append(''.join([chr(b) for b in fuzzed]))
    return variants


def fuzzer(buffer, fuzz_factor=101):
    """Charlie Miller's fuzzer code.

    Takes a buffer of bytes, creates a copy, and replaces some bytes with random values.
    Number of bytes to modify depends on fuzz_factor.

    :param buffer: the data to fuzz.
    :type buffer: bytearray
    :param fuzz_factor: degree of fuzzing.
    :type fuzz_factor: int
    :return: fuzzed buffer
    :rtype: bytearray
    """
    buf = deepcopy(buffer)
    num_writes = random.randrange(math.ceil((float(len(buf)) / fuzz_factor))) + 1
    for _ in range(num_writes):
        random_byte = random.randrange(256)
        random_position = random.randrange(len(buf))
        buf[random_position] = random_byte
    return buf


if __name__ == '__main__':
    fuzzed_contents = fuzz_string(seed_content, 3, 5)
    for fuzzed_content in fuzzed_contents:
        print(fuzzed_content)
        pass
