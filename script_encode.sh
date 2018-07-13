#!/bin/sh

ENCODING_FOLDER="encodings/samsung_andrew"
PICTURES_FOLDER="photos_for_encoding/samsung_andrew"

mkdir -p $ENCODING_FOLDER
for FILENAME in $PICTURES_FOLDER/* ; do
    python fr_encodings.py $FILENAME "andrew chuang" --filename $ENCODING_FOLDER/$(basename $FILENAME)
done
