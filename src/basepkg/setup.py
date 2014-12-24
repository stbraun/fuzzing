"""
basepkg: Some general meta classes.

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2014, Stefan Braun.
Licensed under MIT.
"""
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools_behave import behave_test


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "0.2.1"

setup(name="basepkg",
      version=version,
      description="Some general functions and classes.",
      long_description=open("README.rst").read(),
      classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
      ],
      keywords="development tools",  # Separate with spaces
      author="Stefan Braun",
      author_email="sb@action.ms",
      url="https://github.com/stbraun/basepkg",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest', 'behave>=1.2.4'],
      cmdclass={'test': PyTest,
                'behave_test': behave_test,
                },

      # List of packages that this one depends upon:
      install_requires=['sphinx', 'wrapt'],
      # entry_points={
      #   'console_scripts':
      #       ['basepkg=gp_meta:main']
      # }
)
