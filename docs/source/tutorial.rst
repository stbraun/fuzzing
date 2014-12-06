Tutorial
========

The following sections will show how to use the classes and functions of the package.


Create Singletons
-----------------

A singleton class can be created based on a meta class or using a decorator.
Using the decorator is the preferred way. Meta class will likely be deprecated soon.

Creating a singleton class using the singleton decorator is simple: ::

    from gp_decorators.singleton import singleton

    @singleton
    class SomeClass(object):
        """A singleton class."""
        <your code>



Usage of Singleton meta class with Python3: ::

    from gp_meta.singleton import Singleton

    class SomeClass(object, metaclass=Singleton):
        <your code>

For Python2 use the following syntax: ::

    class SomeClass(object):
        __metaclass__ = Singleton
        <your code



Logging
-------

*[not available yet]*


The base package supports logging based on the standard logging package.

Loggers are named according to the packages, e.g. 'gp_tools'.

Example for a simple configuration in YAML format: ::

    version: 1
    formatters:
      simple:
        format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        level: WARNING
        formatter: simple
        stream: ext://sys.stdout
    loggers:
      gp_tools:
        level: WARNING
        handlers: [console]
        propagate: yes
    root:
      level: WARNING
      handlers: [console]

Important is the logger 'gp_tools' and it's propagate property.


