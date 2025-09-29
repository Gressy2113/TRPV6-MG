#!/bin/bash 

for folder in PS/MG_0.8 PS/CA_0.85 PS-apo/MG_0.8 PS-apo/CA_0.85
do
    nohup python SCRIPTS/block_prot.py $folder 0.5 2 > $folder/block.out & 
    disown
done
