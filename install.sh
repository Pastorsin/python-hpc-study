#!/bin/bash

install_cython_versions() {
    VERSIONS_DIR=$1
    PY_BIN=$2
    COMPILER=$3

    if [[ $COMPILER == "icc" ]]; then
        export LDSHARED="icc -shared"
        export CC=icc
    fi

    cython_versions=$(find $VERSIONS_DIR -type d -name "cython*")

    for cython_version in $cython_versions; do
        echo "--"
        echo $cython_version
        echo "--"

        cd $cython_version
        $PY_BIN setup.py build_ext --inplace
    done
}

case $1 in
    "cython")
        install_cython_versions $2 $3 $4
    ;;
esac
