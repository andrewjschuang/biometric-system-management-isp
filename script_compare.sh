#!/bin/bash

if [[ ($# != 2) || ! (-d "$1" && -d "$2") ]]; then
    echo "Usage: ./script_compare.sh ENCODINGS PICTURES"
    echo "Both arguments should be directories."
    exit 1
fi

ENCODING_FOLDER=$1
PICTURES_FOLDER=$2

printf "ENCODING_FOLDER: %s\nPICTURES_FOLDER: %s\n" "$ENCODING_FOLDER" "$PICTURES_FOLDER"
read -p "Continue? [y/n] "

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    mkdir -p "$PICTURES_FOLDER"/$(basename $ENCODING_FOLDER)
    for FILENAME in $ENCODING_FOLDER/* ; do
        python face_distance_plotter.py --encoding $FILENAME --folder "$PICTURES_FOLDER"
    done
fi
