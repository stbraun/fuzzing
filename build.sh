#usr/bin/env bash

source venv/bin/activate

pip install -r requirements.txt

flake8 --output-file reports/flake8.txt --benchmark --count --statistics fuzzing run_fuzzer.py

nosetests --with-coverage --cover-branches --cover-inclusive --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml tests/

paver sdist

cd docs
make html
