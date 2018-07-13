#!/bin/sh

ENCODING_FOLDER="encodings/canon_small_andrew"
PICTURES_FOLDER="photos_for_Andrew_Chuang/170806 Oficialização dos ministérios"

mkdir -p "$PICTURES_FOLDER"/$(basename $ENCODING_FOLDER)
for FILENAME in $ENCODING_FOLDER/* ; do
    python face_distance_plotter.py --encoding $FILENAME --folder "$PICTURES_FOLDER"
done
