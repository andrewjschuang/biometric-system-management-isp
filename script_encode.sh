#!/bin/bash

if [[ ($# != 3) || ! (-d "$1" && -d "$2") ]]; then
    echo "Usage: ./script_encode.sh ENCODINGS PICTURES NAME"
    echo "ENCODINGS and PICTURES should be directories. NAME is the label."
    exit 1
fi

ENCODING_FOLDER=$1
PICTURES_FOLDER=$2
NAME=$3

printf "ENCODING_FOLDER: %s\nPICTURES_FOLDER: %s\nNAME: %s\n" "$ENCODING_FOLDER" "$PICTURES_FOLDER" "$NAME"
read -p "Continue? [y/n] "

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    mkdir -p $ENCODING_FOLDER
    for FILENAME in $PICTURES_FOLDER/* ; do
        python fr_encodings.py $FILENAME $NAME --filename $ENCODING_FOLDER/$(basename $FILENAME)
    done
fi
