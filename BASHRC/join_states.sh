#!/bin/bash
#объединение отдельных фреймов, полученных с помощью extract_pdb.sh, в один файл 

folder=S5-S6_adapted-MG/mw_0.8/walker_0/state #System.0.ace.MGu/plmd.metad.2d.b5h0.3_r7/state #System.0_FC_bbfix.MGb_FC/METAD.3D.b10h2.5/state  #System.0.MGb/METAD.2D.b10h2.5/state #System.0/METAD.2D.b5.h0.3/state #System.0/MD.0/state
T=2600000 #ps
dt=5000 #ps #100 #1000 #10000 #1000 #10000 #4000 #шаг в пс
nmin=0 #1000 #0
file=../all_T_$T\_dt_$dt.pdb
prefix="_state t_"

imax=$((($T-$nmin) / $dt)) #8 #20 #50 #50 #20 #20 #38 #50 #50
echo $imax
nmax=$(($imax*$dt))

cd $folder
pwd
rm -f $file
cat "${prefix}$nmin.pdb" >> $file
for ((i=1;i<=$imax;i=i+1));
do
    echo "MODEL $i" >> $file
    n=$(($nmin + $i*$dt))
    echo $n
    awk 'FNR>2' "${prefix}$n.pdb" >> $file
done
