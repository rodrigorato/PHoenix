#!/bin/bash

SLICES_DIR="./proj-slices"

for slice in $SLICES_DIR/*.json; do
    echo Running slice $slice
    ./analyser.py $slice
    echo 'done with' $slice
    read
done;

