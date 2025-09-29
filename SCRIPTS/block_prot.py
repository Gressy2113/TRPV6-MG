import plumed
import numpy as np

import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append('./')  

from func_read import read_fes_3d
from func_reweight import reweight_3d

from tqdm import tqdm

'''
PARAMS
'''
FOLDER = sys.argv[1]
Tmin = float(sys.argv[2])
Tmax = float(sys.argv[3])

print(FOLDER, Tmin, Tmax)

DATA_FOLDER = 'Reweighting_data'


'''
RUN BLOCK ANALYSIS
'''
cvlr = plumed.read_as_pandas(f'{FOLDER}/COLVAR')
COLVAR = cvlr[(Tmin*1000**2 <= cvlr['time']) & (cvlr['time'] <= Tmax*1000**2)]


dist1, dist2, cn, fes, Nbins_D1, Nbins_D2, Nbins_CN, Bonds_D1, Bonds_D2, Bonds_CN = read_fes_3d(FOLDER, NAME = '80')

N_blocks = np.arange(3, 25, 1)

print(COLVAR)

dG1_mean = np.zeros_like(N_blocks).astype(float)
dG1_std = np.zeros_like(N_blocks).astype(float)

dG2_mean = np.zeros_like(N_blocks).astype(float)
dG2_std = np.zeros_like(N_blocks).astype(float)

for i in tqdm(range(len(N_blocks))): 
    dG1_cur, dG2_cur = [], []
    dt = len(COLVAR)//N_blocks[i]
    print(len(COLVAR), N_blocks[i], dt)
    for j in range(0, len(COLVAR), dt):
        dG1_, dG2_ = reweight_3d(COLVAR[j:j+dt], 
                                    dist1, dist2, cn, fes, 
                                    Nbins_D1, Nbins_D2, Nbins_CN, Bonds_D1, Bonds_D2, Bonds_CN, 
                                    FOLDER, DATA_FOLDER, FSAVE=False
                                )

        if np.isnan(dG1_) == False and dG1_ < np.inf and dG1_ > -np.inf:
            dG1_cur.append(dG1_)
        if np.isnan(dG2_) == False and dG2_ < np.inf and dG2_ > -np.inf:
            dG2_cur.append(dG2_)
    print(dG1_mean, dG1_std, dG2_mean, dG2_std)
    dG1_mean[i] = np.nanmean(dG1_cur)
    dG1_std[i] = np.nanstd(dG1_cur, ddof=1)/np.sqrt(len(dG1_cur)) 
    
    dG2_mean[i] = np.nanmean(dG2_cur)
    dG2_std[i] = np.nanstd(dG2_cur, ddof=1)/np.sqrt(len(dG2_cur)) 

np.savetxt(f'{FOLDER}/{DATA_FOLDER}/block_analysis.csv', 
        np.vstack([N_blocks, dG1_mean, dG1_std, dG2_mean, dG2_std]).T, 
        header = 'N_blocks dG1_mean dG1_std dG2_mean dG2_std')
    