#!bin/bash

# for SYS in S5-S6_adapted-MG/MD #S5-S6_adapted-CA/MD 
# do
    # cd /home/veretenenko/TRPV6-Mg/ScaledTopology-final/$SYS
    # mkdir -p dihedral
    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.ch1_489 > nohup_ch1_489.out & 

    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.ch2_489 > nohup_ch2_489.out & 

    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.ch1_580 > nohup_ch1_580.out & 

    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.ch2_580 > nohup_ch2_580.out & 
    #mkdir -p dist
    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.ca > nohup_ca.out & 

    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.cg > nohup_cg.out & 
    
    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.mg_489od1 > nohup_mg_489od1.out & 

    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.mg_489od2 > nohup_mg_489od2.out & 

    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.mg_580od1 > nohup_mg_580od1.out & 

    # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../IMPULSE/calc_gp.mk \
    #             -f ../../IMPULSE/args_gp/args.mg_580od2 > nohup_mg_580od2.out & 

# done

for SYS in S5-S6_apo-MG/mw_0.8 #S5-S6_apo-CA/mw_0.85 S5-S6_adapted-CA/mw_0.85 #S5-S6_apo-MG/mw_0.8 #S5-S6_adapted-CA/mw_0.85 S5-S6_adapted-MG/mw_0.8 \
                #S5-S6_apo-CA/mw_0.85 S5-S6_apo-MG/mw_0.8
do
    cd /home/veretenenko/TRPV6-Mg/ScaledTopology-final/$SYS
    for i in 3 0 1 2 #3 0
    do
        cd walker_$i

        # mkdir -p crd
        # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/crd.mk \
        #             -f ../../../IMPULSE/args.crd > nohup_state.out & 

        # mkdir -p state
        # nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t /home/veretenenko/Soft/Common_scripts/Post/state.mk \
        #             -f ../../../IMPULSE/args.state > nohup_state.out & 

        nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
                    -f ../../../IMPULSE/args_gp/args.ch1_489 > nohup_ch1_489.out & 

        nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
                    -f ../../../IMPULSE/args_gp/args.ch2_489 > nohup_ch2_489.out & 

        nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
                    -f ../../../IMPULSE/args_gp/args.ch1_580 > nohup_ch1_580.out & 

        nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
                    -f ../../../IMPULSE/args_gp/args.ch2_580 > nohup_ch2_580.out & 
        cd ../
    done

done

# for SYS in S5-S6_adapted-CA/mw_0.85 S5-S6_adapted-MG/mw_0.8  #S5-S6_apo-CA/mw_0.85 S5-S6_apo-MG/mw_0.8 #\
#            #S5-S6_adapted-CA/mw_0.85 S5-S6_adapted-MG/mw_0.8 
# do
#     cd /home/veretenenko/TRPV6-Mg/ScaledTopology-final/$SYS
#     for i in 0 1 2 3
#     do
#         cd walker_$i
#         mkdir -p dist
#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.ca > nohup_ca.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.cg > nohup_cg.out & 

#         cd ../
#     done

# done


# for SYS in S5-S6_adapted-CA/mw_0.85 S5-S6_apo-CA/mw_0.85
# do
#     cd /home/veretenenko/TRPV6-Mg/ScaledTopology-final/$SYS
#     for i in 0 1 2 3
#     do
#         cd walker_$i

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.ca_489od1 > nohup_ca_489od1.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.ca_489od2 > nohup_ca_489od2.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.ca_580od1 > nohup_ca_580od1.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.ca_580od2 > nohup_ca_580od2.out & 
#         cd ../
#     done

# done

# for SYS in S5-S6_apo-MG/mw_0.8 #S5-S6_adapted-MG/mw_0.8 #S5-S6_apo-MG/mw_0.8
# do
#     cd /home/veretenenko/TRPV6-Mg/ScaledTopology-final/$SYS
#     for i in 2 3 #
#     do
#         cd walker_$i

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.mg_489od1 > nohup_mg_489od1.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.mg_489od2 > nohup_mg_489od2.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.mg_580od1 > nohup_mg_580od1.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.mg_580od2 > nohup_mg_580od2.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.ca > nohup_ca.out & 

#         nohup /nfs/belka2/soft/impulse/dev/inst/runtask.py -t ../../../IMPULSE/calc_gp.mk \
#                     -f ../../../IMPULSE/args_gp/args.cg > nohup_cg.out & 

#         cd ../
#     done

# done

