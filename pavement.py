""" Provide tasks for build and deployment.

This file provides tasks for paver.
"""

from paver.easy import *
from paver.doctools import html, doc_clean
from paver.setuputils import setup
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import sys


sys.path.insert(0, './')


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


version = '0.3.3'

setup(name="fuzzing",
      version=version,
      description="Tools for stress testing applications.",
      long_description=open("README.rst").read(),
      classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
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


options(
    sphinx=Bunch(
        builddir="build",
        sourcedir="source",
    )
)


@task
def clean():
    """Remove build artifacts."""
    sh('rm -rf build dist')


@task
def test_coverage():
    """Run nosetests with coverage."""
    sh('nosetests --with-coverage --cover-branches --cover-inclusive --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml tests/ ')


@task
def analyze():
    """Analyze project using flake8."""
    sh("rm -f reports/flake8.txt")
    sh("flake8 --output-file reports/flake8.txt --benchmark --count --statistics fuzzing run_fuzzer.py")


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass


@task
@needs('doc_clean', 'html')
def docs():
    """Rebuild documentation."""
    pass


@task
@needs('clean', 'test_coverage', 'analyze', 'sdist', 'docs')
def build():
    """Perform a complete build."""
    pass
