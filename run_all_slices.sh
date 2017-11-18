#!/bin/bash

SLICES_DIR="./proj-slices"

for slice in $SLICES_DIR/*.json; do
    echo Running slice $slice
    ./analyser.py $slice
    echo -e 'done with $slice \n\n\n\n\n\n\n'
done;

