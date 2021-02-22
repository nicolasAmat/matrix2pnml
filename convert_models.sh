#!/bin/bash

# Convert all incidence matrices in a given directory into .pnml

shopt -s nullglob

models=$1

for F in ${1}/*.pnh; do
    echo "${F%.pnh}.pnml"
    ./matrix2pnml.py $F
done

exit 0
