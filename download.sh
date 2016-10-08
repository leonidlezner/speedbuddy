#!/usr/bin/env bash

mkdir -p data

cd data

wget -N http://www.radarfalle.de/POI/download/garmin-mobil.zip

unzip -o garmin-mobil.zip -d garmin-mobil

rm garmin-mobil.zip