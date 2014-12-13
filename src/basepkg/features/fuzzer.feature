# Created by sb at 06.12.14
Feature: Provide a fuzz tester.
  A fuzz tester consists of a tests data generator,
  a driver feeding data to the SUT (Software Under Test),
  and an oracle detecting success or failure of a test run.

  | Test given applications with fuzzed files. Count successful and failed calls.
  | Call a given application with a file that was fuzzed before.
  | Example: Take a jpeg file, fuzz it and call Preview with the fuzzed file.

  # The exact number of modified bytes can't be guaranteed.
  # This is because a byte will be replaced with a random value which
  # may be the same as already there.
  # Therefore only the maximum number of modified bytes is known.
  Scenario: Fuzz a binary buffer with minimum number of modifications.
    Given a byte array of len 10
    When feeding it into the fuzzer, setting the fuzz_factor to 10
    Then it will return a buffer with up to two modified bytes.

  Scenario Outline: Fuzz a binary buffer with different numbers of modifications.
    Given a byte array of len 10
    When feeding it into the fuzzer, setting the fuzz_factor to <fuzz_factor>
    Then it will return a buffer with up to <max_modified> modified bytes.

    Examples:
    | fuzz_factor | max_modified |
    |           1 |           10 |
    |           5 |            3 |
    |          11 |            2 |
    |         101 |            2 |


  Scenario Outline: Create a list of fuzzed variants of a given string.
    Given a string as seed.
    """
      Create fuzzed variants of this string.
      A test seed for our fuzz tester.
      Multiple lines are fine.
      """
    When feeding the seed into the fuzzer, providing a count of <count>
    Then it will return a list of <len_list> fuzzed variants of the seed.

    Examples:
    | count | len_list |
    |     0 |        0 |
    |     1 |        1 |
    |    11 |       11 |
    |   101 |      101 |


  @slow
  Scenario Outline: File fuzzer
    Given a list of file paths
    | file_path              |
    | ./features/data/t1.pdf |
    | ./features/data/t2.jpg |
    | ./features/data/t3.pdf |
    And a list of applications
    | application                                                               |
    | /Applications/Adobe Reader 9/Adobe Reader.app/Contents/MacOS/AdobeReader  |
    | /Applications/Preview.app/Contents/MacOS/Preview                          |
    And a FuzzExecutor instance created with those lists.
    When running a test <runs> times
    Then a randomly chosen application will be called with a randomly chosen file.
    And <runs> results are recorded.

    Examples: Test runs
    | runs |
    |    0 |
    |    1 |
    |    2 |
    |   11 |
