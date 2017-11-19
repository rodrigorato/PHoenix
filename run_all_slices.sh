#!/bin/bash

SLICES_DIR="./proj-slices"

for slice in $SLICES_DIR/slice{1..11}.json; do
    clear;
    echo Running slice $slice
    echo 
    ./analyser.py $slice
    echo
    echo 'done with' $slice
    read
done;

