#!/bin/bash 

for folder in PS/MG_0.8 PS/CA_0.85 #PS-apo/MG_0.8 PS-apo/CA_0.85
do
    nohup python SCRIPTS/plotstring.py $folder 200 200 MFEP > $folder/plotstring.out & 
done