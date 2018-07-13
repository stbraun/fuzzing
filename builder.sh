#!/usr/bin/env bash

export PATH=/usr/local/bin:/usr/local/sbin:$PATH

# prepare folder for build reports
if [ -d reports ]; then
    echo "report folder exists already."
else
    mkdir reports
fi

if [ -z "$1" ]; then
    echo 'usage: builder.sh <cmd>'
    exit 1;
fi


mk_venv() {
    # setup virtual environment ...
    if python3 -m venv venv; then
        echo "===============================";
        echo " virtual environment installed ";
        echo "===============================";
    else
        exit 1;
    fi
}

activate_venv() {
    # activate virtual environment
    echo "activate virtual environment ..."
    source venv/bin/activate
}

install_requirements() {
    # install required packages
    pip install --upgrade pip
    if pip install -r requirements.txt; then
        echo "======================";
        echo "requirements installed";
        echo "======================";
    else
        exit 1;
    fi
}

check_sources() {
    # run sanity checks
    if flake8 --output-file reports/flake8.txt --benchmark --count --statistics fuzzing gp_decorators run_fuzzer.py; then
        echo "=====================";
        echo " sanity tests passed ";
        echo "=====================";
    else
        echo "=====================";
        echo " sanity tests failed ";
        echo "=====================";

        exit 1;
    fi

    if pylint --rcfile=resrc/pylintrc fuzzing gp_decorators run_fuzzer.py | tee reports/pylint.txt; then
        echo "========================";
        echo " static analysis passed";
        echo "========================";
    else
        echo "========================";
        echo " static analysis failed ";
        echo "========================";
        exit 1;
    fi
}

run_tests() {
    # run test and measure coverage
    if nosetests --cover-package=fuzzing --with-coverage --cover-branches --cover-inclusive --with-xunit --xunit-file=reports/nosetests.xml --cover-html --cover-html-dir=reports/coverage --cover-xml --cover-xml-file=reports/coverage.xml tests/ ; then
        echo "===================";
        echo " unit tests passed ";
        echo "===================";
    else
        echo "===================";
        echo " unit tests failed ";
        echo "===================";
        exit 1;
    fi

    # run behave tests
    if behave | tee reports/behave.txt; then
        echo "=========================";
        echo " behavioral tests passed ";
        echo "=========================";
    else
        echo "=========================";
        echo " behavioral tests failed ";
        echo "=========================";
        exit 1;
    fi
}

create_dist() {
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
}

case "$1" in
    venv )
        mk_venv;
        ;;
    requ )
        activate_venv;
        install_requirements;
        ;;
    checks )
        activate_venv;
        check_sources;
        ;;
    tests )
        activate_venv;
        run_tests;
        ;;
    dist )
        activate_venv;
        create_dist;
        ;;
    all )
        mk_venv;
        activate_venv;
        install_requirements;
        check_sources;
        run_tests;
        create_dist;
        ;;
esac
exit 0
