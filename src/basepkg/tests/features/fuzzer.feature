# Created by sb at 06.12.14
Feature: Provide a fuzz tester
  A fuzz tester consists of a tests data generator,
  a driver feeding data to the SUT (Software Under Test),
  and an oracle detecting success or failure of a test run.

  # The exact number of modified bytes can't be guaranteed.
  # This is because a byte will be replaced with a random value which
  # may be the same as already there.
  # Therefore only the maximum number of modified bytes is known.
  Scenario: Fuzz a binary buffer with minimum number of modifications.
    Given a bytearray of len 10
    When feeding it into the fuzzer, setting the fuzz_factor to 10
    Then it will return a buffer with up to two modified bytes.

  Scenario: Fuzz a binary buffer with maximum number of modifications.
    Given a bytearray of len 10
    When feeding it into the fuzzer, setting the fuzz_factor to 1
    Then it will return a buffer with up to 10 modified bytes.

  Scenario: Create a list of fuzzed variants of a given string.
    Given a string as seed.
    When feeding the seed into the fuzzer, providing a count of 5
    Then it will return a list of 5 fuzzed variants of the seed.