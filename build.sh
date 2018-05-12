#!/usr/bin/env bash

# prepare folder for build reports
mkdir reports

# setup virtual environment ...
python3 -m venv venv

# ... and activate it
echo "activate virtual environment ..."
source venv/bin/activate

# install required packages
pip install --upgrade pip
if pip install -r requirements.txt; then
    echo "======================";
    echo "requirements installed";
    echo "======================";
else
    exit 1;
fi

# run sanity checks
if flake8 --output-file reports/flake8.txt --benchmark --count --statistics fuzzing gp_decorators run_fuzzer.py; then
    echo "=====================";
    echo " sanity tests passed";
    echo "=====================";
else
    exit 1;
fi

if pylint --rcfile=resrc/pylintrc fuzzing gp_decorators run_fuzzer.py | tee reports/pylint.txt; then
    echo "========================";
    echo " static analysis passed";
    echo "========================";
else
    exit 1;
fi

# run test and measure coverage
if nosetests --with-coverage --cover-branches --cover-inclusive --with-xunit --xunit-file=reports/nosetests.xml --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml tests/  > reports/nosetest.txt 2>&1; then
   echo "=================";
   echo "unit tests passed";
   echo "=================";
else
   exit 1;
fi

# run behave tests
if behave | tee reports/behave.txt; then
   echo "=======================";
   echo "behavioral tests passed";
   echo "=======================";
else
   exit 1;
fi

# build source distribution tarball
python setup.py sdist

# install package ...
python setup.py install

# ... and generate documentation
pushd docs
make html
popd

# package documentation
echo "package documentation ..."
pushd docs/build
zip -r ../../dist/fuzzing-docs.zip html
popd

rm -rf fuzzing.egg-info
rm dist/*.egg
