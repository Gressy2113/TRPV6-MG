#!bin/bash

# Join COLVAR.# from multiple walkers into one file

for folder in PS/MG_0.8 PS/CA_0.85 PS-apo/MG_0.8 PS-apo/CA_0.85
do
    cd $folder
    paste -d "\n" walker_0/COLVAR.0 \
                    walker_1/COLVAR.1 \
                    walker_2/COLVAR.2 \
                    walker_3/COLVAR.3 > COLVAR
    head -n -3 COLVAR > tmp && mv tmp COLVAR
    rm -f tmp
    cd ../../
done