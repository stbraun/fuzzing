#!/usr/bin/env bash

# prepare folder for build reports
mkdir reports

# setup virtual environment ...
python3 -m venv venv

# ... and activate it
echo "activate virtual environment ..."
source venv/bin/activate

# install required packages
pip install -r requirements.txt

# run sanity checks
flake8 --output-file reports/flake8.txt --benchmark --count --statistics fuzzing gp_decorators run_fuzzer.py

pylint --rcfile=resrc/pylintrc fuzzing gp_decorators | tee reports/pylint.txt

# run test and measure coverage
nosetests --with-coverage --cover-branches --cover-inclusive --with-xunit --xunit-file=reports/nosetests.xml --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml tests/

# run behave tests
behave | tee reports/behave.txt

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
