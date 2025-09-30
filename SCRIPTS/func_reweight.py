import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import matplotlib
import os

from SCRIPTS.constants import *
from SCRIPTS.func_main import dG_calc

matplotlib.rcParams['svg.fonttype'] = 'none'


def reweight_plot_2d(COLVAR, dist, cn, fes, Nbins_D, Nbins_CN, Bonds_D, Bonds_CN, FOLDER, 
                DATA_FOLDER = 'Reweighting_data', FSAVE = True): 
    Ubias = -fes.T * (1-1/BIASF)
    
    WEIGHTS, ED = np.histogramdd(COLVAR[['dp', 'cn']].to_numpy(), 
                                bins = [Nbins_D, Nbins_CN],
                                range = (Bonds_D, Bonds_CN),
                                density=True, 
                                )
    weighted_avg = np.exp(1/kBT * (Ubias-np.max(Ubias))) * WEIGHTS
    norm = np.sum(np.exp(1/kBT * (Ubias-np.max(Ubias))))

    FES_2D = -kBT * np.log(weighted_avg/norm)
    FES_2D[FES_2D==np.inf] = np.nanmax(FES_2D[FES_2D<np.inf])

    # if plot: 
    #     fig, ax = plt.subplots()
    #     ax.set_box_aspect(1)
    #     vmax = np.nanmax(FES_2D)//10 * 10
    #     h = plt.contourf(dist[0], cn[:, 0], FES_2D.T, 
    #                 cmap = 'jet', 
    #                 origin = 'lower',
    #                 levels = np.arange(0, vmax, 1), 
    #                 )

    #     plt.contour(dist[0], cn[:, 0], FES_2D.T, 
    #                 colors = 'k', 
    #                 linewidths=0.5,
    #                 levels = np.arange(0, vmax, 10)
    #                 )
        
    #     plt.xlim(0., 2)
        
    #     plt.colorbar(h, label="Free energy, kJ/mol")
    #     plt.xlabel('d, nm')
    #     plt.ylabel("CN")
    #     plt.title(FOLDER)
    #     plt.savefig(f'{FOLDER}/{IMAGE_FOLDER}/FES_2D_reweighting.svg', dpi=300, bbox_inches = 'tight')
    #     plt.show()

    ####1D####

    weighted_avg = np.sum(np.exp(1/kBT * (Ubias-np.max(Ubias))) * WEIGHTS, axis=1)
    weighted_avg[weighted_avg==0]=np.nan
    norm = np.sum(np.exp(1/kBT * (Ubias-np.max(Ubias))))

    PMF = -kBT * np.log(weighted_avg/norm)

    is_bulk=np.int_((L_BULK_MIN < dist[0]) & (dist[0] < L_BULK_MAX))
    shift = np.nansum(is_bulk*PMF)/np.nansum(is_bulk)
    PMF-=shift
    _, _, _, dG = dG_calc(dist[0], PMF, SYSTEM=FOLDER)
    
    if FSAVE: 
        if not os.path.exists(f'{FOLDER}/{DATA_FOLDER}'):
            os.mkdir(f'{FOLDER}/{DATA_FOLDER}')
            
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/fes_dens_2D.csv', FES_2D)
        
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/Prof_1D.dat', np.concatenate(([dist[0]], [PMF])).T)

    # if plot:        
    #     fig, ax = plt.subplots(figsize = (5.5, 3))
    #     plt.plot(dist[0], PMF, '.-', color = 'blue', label = f'dG={round(dG0, 3)} kJ/mol')
    #     ax.grid(True, which='major', linestyle=  '-')
    #     ax.grid(True, which='minor', linestyle=  '-', lw=0.2)

    #     plt.xlim(0, 2)
    #     plt.legend()
    #     plt.xlabel('L, nm')
    #     plt.ylabel('Free Energy, kJ/mol')
    #     plt.savefig(f'{FOLDER}/PMF_reweight.svg', dpi=300, bbox_inches = 'tight')
    #     plt.show()


    return (dG)

def reweight_3d(COLVAR,
                dist1, dist2, cn, fes, 
                Nbins_D1, Nbins_D2, Nbins_CN, Bonds_D1, Bonds_D2, Bonds_CN, 
                FOLDER = None, DATA_FOLDER = 'Reweighting_data', FSAVE=True): 
    
    if not os.path.exists(f'{FOLDER}/{DATA_FOLDER}'):
        os.mkdir(f'{FOLDER}/{DATA_FOLDER}')

    Ubias = -fes * (1-1/BIASF)

    WEIGHTS, ED = np.histogramdd(COLVAR[['cn', 'd_580', 'd_489']].to_numpy(), #[tstart:tfinal], 
                                bins = [Nbins_CN, Nbins_D2, Nbins_D1],
                                range = (Bonds_CN, Bonds_D2, Bonds_D1),
                                density=True, 
                                )
    weighted_avg = np.sum(np.exp(1/kBT * Ubias) * WEIGHTS, axis=0)
    weighted_avg[weighted_avg==0]=np.nan
    norm = np.sum(np.exp(1/kBT * (Ubias-np.max(Ubias))))
    fes_dens = -kBT * np.log(weighted_avg/norm)

    ####1D####

    ###d1###
    dist = dist1[0, 0, :]
    dist_dens = np.sum(np.exp(1/kBT * Ubias) * WEIGHTS, axis=(0, 1))
    dist_fes = -kBT * np.log(dist_dens/norm)
    
    is_bulk=np.int_((L_BULK_MIN < dist) & (dist < L_BULK_MAX))
    shift = np.nansum(is_bulk*dist_fes)/np.nansum(is_bulk) #np.mean(dist_fes[is_bulk==1]) #/np.sum(is_bulk)
    dist_fes -= shift
    dG_PMF, dG_R, dG_I, dG0_489 = dG_calc(dist, dist_fes, FOLDER)
    print(dG_PMF, dG_R, dG_I, dG0_489)
    if FSAVE: 
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/d1.csv', np.vstack((dist, dist_fes)))

    ###d2###
    dist = dist2[0, :, 0]
    dist_dens = np.sum(np.exp(1/kBT * Ubias) * WEIGHTS, axis=(0, 2))
    dist_fes = -kBT * np.log(dist_dens/norm)
    
    is_bulk=np.int_((L_BULK_MIN < dist) & (dist < L_BULK_MAX))
    shift = np.nansum(is_bulk*dist_fes)/np.nansum(is_bulk) #np.mean(dist_fes[is_bulk==1]) #/np.sum(is_bulk)
    dist_fes -= shift
    dG_PMF, dG_R, dG_I, dG0_580 = dG_calc(dist, dist_fes, FOLDER)
    print(dG_PMF, dG_R, dG_I, dG0_580)
    if FSAVE: 
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/d2.csv', np.vstack((dist, dist_fes)))

    if FSAVE: 
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/fes_dens_2D.csv', fes_dens)

    ###
    return (dG0_489, dG0_580)

