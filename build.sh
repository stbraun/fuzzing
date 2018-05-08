#usr/bin/env bash

source venv/bin/activate

rm -rf .coveraage
rm -rf reports
mkdir reports
rm -rf venv

python3 -m venv venv

pip install -r requirements.txt

flake8 --output-file reports/flake8.txt --benchmark --count --statistics fuzzing run_fuzzer.py

pylint --rcfile=resrc/pylintrc fuzzing > reports/pylint.txt

nosetests --with-coverage --cover-branches --cover-inclusive --with-xunit --xunit-file=reports/nosetests.xml --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml tests/

paver sdist

python setup.py install

cd docs
make html
