#usr/bin/env bash

# prepare folder for build reports
mkdir reports

# setup virtual environment ...
python3 -m venv venv

# ... and activate it
source venv/bin/activate

# install required packages
pip install -r requirements.txt

# run sanity checks
flake8 --output-file reports/flake8.txt --benchmark --count --statistics fuzzing run_fuzzer.py

pylint --rcfile=resrc/pylintrc fuzzing > reports/pylint.txt

# run test and measure coverage
nosetests --with-coverage --cover-branches --cover-inclusive --with-xunit --xunit-file=reports/nosetests.xml --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml tests/

# build source distribution tarball
python setup.py sdist

# install package ...
python setup.py install

rm -rf fuzzing.egg-info
rm dist/*.egg

# ... and generate documentation
cd docs
make html

# package documentation
cd build
zip -r ../../dist/fuzzing-docs.zip html
