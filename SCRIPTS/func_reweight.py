import numpy as np
import matplotlib
import os

from SCRIPTS.constants import *
from SCRIPTS.func_main import dG_calc

matplotlib.rcParams['svg.fonttype'] = 'none'


def reweight_2d(COLVAR, dist, cn, fes, Nbins_D, Nbins_CN, Bonds_D, Bonds_CN, FOLDER, 
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

    ####1D####

    weighted_avg = np.sum(np.exp(1/kBT * (Ubias-np.max(Ubias))) * WEIGHTS, axis=1)
    weighted_avg[weighted_avg==0]=np.nan
    norm = np.sum(np.exp(1/kBT * (Ubias-np.max(Ubias))))

    PMF = -kBT * np.log(weighted_avg/norm)

    is_bulk=np.int_((L_BULK_MIN < dist[0]) & (dist[0] < L_BULK_MAX))
    shift = np.nansum(is_bulk*PMF)/np.nansum(is_bulk)
    PMF-=shift
    dG_PMF, dG_R, dG_I, dG0 = dG_calc(dist[0], PMF, SYSTEM=FOLDER)
    
    if FSAVE: 
        if not os.path.exists(f'{FOLDER}/{DATA_FOLDER}'):
            os.mkdir(f'{FOLDER}/{DATA_FOLDER}')
            
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/fes_dens_2D.csv', FES_2D)
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/prof_1D.csv', np.concatenate(([dist[0]], [PMF])).T)
        np.savetxt(f'{FOLDER}/{DATA_FOLDER}/cn.csv', cn[:, 0])

    return (dG_PMF, dG_R, dG_I, dG0)

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


def calc_dG_stride_reweight(COLVAR, dist, cn, fes, Nbins_DP, Nbins_CN, Bonds_DP, Bonds_CN, FOLDER):
    N_blocks = np.arange(3, 100, 5)

    dG0_mean = np.zeros_like(N_blocks).astype(float)
    dG0_std = np.zeros_like(N_blocks).astype(float)

    for i in range(len(N_blocks)): 
        dG0_cur = []
        dt = len(COLVAR)//N_blocks[i]
        for j in range(0, len(COLVAR), dt):
            _, _, _, dG0_ = reweight_2d(COLVAR[j:j+dt], dist, cn, fes, Nbins_DP, Nbins_CN, Bonds_DP, Bonds_CN, FOLDER, FSAVE=False)
            if np.isnan(dG0_) == False and dG0_ < np.inf and dG0_ > -np.inf:
                dG0_cur.append(dG0_)
                
        dG0_mean[i] = np.mean(dG0_cur)
        dG0_std[i] = np.std(dG0_cur, ddof=1)/np.sqrt(len(dG0_cur)) #len(np.where(~np.isnan(dG_cur))[0])  #scipy.stats.sem(dG_cur, nan_policy='omit') #np.nanstd(dG_cur) / np.sqrt(len(dG_cur[~np.isnan(dG_cur)]))

    return (N_blocks, dG0_mean, dG0_std)

