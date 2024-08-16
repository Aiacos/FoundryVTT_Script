#!/bin/bash

wget -O /DATA/DnD/01_Data/06_Forgotten_Adventures/FA_Mapmaking_Pack.zip "$1"
rm -fr /DATA/DnD/01_Data/06_Forgotten_Adventures/FA_Mapmaking_Pack
unzip -q /DATA/DnD/01_Data/06_Forgotten_Adventures/FA_Mapmaking_Pack.zip -d /DATA/DnD/01_Data/06_Forgotten_Adventures/
rm -fr FA_Mapmaking_Pack.zip
