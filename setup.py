"""
fuzzing: Some general meta classes.

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.
Currently all tests are written for behave!

Copyright 2015, Stefan Braun.
Licensed under MIT.
"""
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """This is a plug-in for setuptools.

     It will invoke py.test when you run python setup.py test
    """
    def finalize_options(self):
        """Configure."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Execute tests."""
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = '0.3.2'

setup(name="fuzzing",
      version=version,
      description="Tools for stress testing applications.",
      long_description=open("README.rst").read(),
      classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
      ],
      keywords="development tools",  # Separate with spaces
      author="Stefan Braun",
      author_email="sb@action.ms",
      url="https://github.com/stbraun/fuzzing",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest', 'behave>=1.2.4'],
      cmdclass={'test': PyTest},
      scripts=['run_fuzzer.py', ],

      # List of packages that this one depends upon:
      install_requires=['sphinx', 'wrapt', 'PyYAML', 'argh', 'pathtools', 'setuptools'],
      requires=['sphinx', 'wrapt', 'PyYAML', 'argh', 'pathtools', 'setuptools'],
      provides=['fuzzing', 'gp_decorators'],
      # entry_points={
      #   'console_scripts':
      #       ['fuzzing=fuzzing:main']
      # }
)
