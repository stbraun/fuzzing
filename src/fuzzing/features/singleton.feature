# Created by sb at 07.12.14
Feature: Provide support for implementation of singleton classes.
  Make it easy to write and identify singletons.

  Scenario: The singleton capability does not modify the functional behavior of a class.
    Given two functionally identical classes, one is a singleton.
    When creating an instance of the non-singleton class
    And  creating an instance of the singleton class
    Then the functional behavior is identical.

  Scenario: All objects created from a singleton are identical.
    Given a singleton class.
    When creating multiple objects from the class
    Then all will be identical.

  Scenario: A change to a singleton object is visible to all references.
    Given a singleton class.
    When creating multiple objects from the class
    And modifying the value of an attribute in one of them
    Then this modification is visible to all.

  @wip
  Scenario: A singleton class shall report their own type not 'function' (basepkg-47).
    Given a singleton class.
    Then type() shall return the class.

  @wip
  Scenario: A singleton class shall report their own module (basepkg-47).
    Given a singleton class.
    Then __module__ shall be the module of the class.
