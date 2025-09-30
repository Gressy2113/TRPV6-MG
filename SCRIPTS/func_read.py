import numpy as np
import plumed
import pandas as pd


def read_fes_2d(FOLDER, NAME = '30'):    
    data = plumed.read_as_pandas(f"{FOLDER}/FES/{NAME}.dat")

    CV = ['dp', 'cn']
    
    Nbins_DP, Nbins_CN=0,0
    Bonds_DP, Bonds_CN=[-1, -1], [-1, -1]

    with open(f'{FOLDER}/FES/{NAME}.dat', 'r') as f: 
        ss = f.readlines()
        for s in [ss[_] for _ in np.where([s[:2] == '#!' for s in ss])[0]]: 
            s1 = s.split()
            if s1[2] == f'nbins_{CV[0]}': 
                Nbins_DP = int(s1[3])
            elif s1[2] == f'nbins_{CV[1]}': 
                Nbins_CN = int(s1[3])
            elif s1[2] == f'min_{CV[0]}': 
                Bonds_DP[0] = float(s1[3])
            elif s1[2] == f'max_{CV[0]}':
                Bonds_DP[1] = float(s1[3])
            elif s1[2] == f'min_{CV[1]}': 
                Bonds_CN[0] = float(s1[3])
            elif s1[2] == f'max_{CV[1]}':
                Bonds_CN[1] = float(s1[3])
    print(Nbins_DP, Nbins_CN, Bonds_DP, Bonds_CN)

    dist = np.array(data[CV[0]]).reshape((Nbins_CN, Nbins_DP))
    cn = np.array(data[CV[1]]).reshape((Nbins_CN, Nbins_DP))

    fes    = np.array(data["file.free"]).reshape((Nbins_CN, Nbins_DP)) #* m

    return (dist, cn, fes, Nbins_DP, Nbins_CN, Bonds_DP, Bonds_CN)

def read_fes_3d(FOLDER, NAME='80'):    
    data = plumed.read_as_pandas(f"{FOLDER}/FES/{NAME}.dat")

    CV = ['d_489', 'd_580', 'cn']
    
    Nbins_D1, Nbins_D2, Nbins_CN=0,0,0
    Bonds_D1, Bonds_D2, Bonds_CN=[-1, -1], [-1, -1], [-1, -1]
    with open(f'{FOLDER}/FES/{NAME}.dat', 'r') as f: 
        for s in f.readlines():
        #for s in [ss[_] for _ in np.where([s[:2] == '#!' for s in ss])[0]]: 
            if s[0] != '#': 
                break
            s1 = s.split()
            if s1[2] == f'nbins_{CV[0]}': 
                Nbins_D1 = int(s1[3])
            elif s1[2] == f'nbins_{CV[1]}': 
                Nbins_D2 = int(s1[3])
            elif s1[2] == f'nbins_{CV[2]}': 
                Nbins_CN = int(s1[3])
                
            elif s1[2] == f'min_{CV[0]}': 
                Bonds_D1[0] = float(s1[3])
            elif s1[2] == f'max_{CV[0]}':
                Bonds_D1[1] = float(s1[3])
            elif s1[2] == f'min_{CV[1]}': 
                Bonds_D2[0] = float(s1[3])
            elif s1[2] == f'max_{CV[1]}':
                Bonds_D2[1] = float(s1[3])
            elif s1[2] == f'min_{CV[2]}': 
                Bonds_CN[0] = float(s1[3])
            elif s1[2] == f'max_{CV[2]}':
                Bonds_CN[1] = float(s1[3])
    print(Nbins_D1, Nbins_D2, Nbins_CN, Bonds_D1, Bonds_D2, Bonds_CN)

    dist1 = np.array(data[CV[0]]).reshape((Nbins_CN, Nbins_D2, Nbins_D1))
    dist2 = np.array(data[CV[1]]).reshape((Nbins_CN, Nbins_D2, Nbins_D1))
    cn = np.array(data[CV[2]]).reshape((Nbins_CN, Nbins_D2, Nbins_D1))
    fes    = np.array(data["file.free"]).reshape((Nbins_CN, Nbins_D2, Nbins_D1)) 

    return (dist1, dist2, cn, fes,  Nbins_D1, Nbins_D2, Nbins_CN, Bonds_D1, Bonds_D2, Bonds_CN) 


def read_fes(FOLDER, DATA_FOLDER = 'Reweighting_data'):
    fes_2d = pd.read_csv(f'{FOLDER}/{DATA_FOLDER}/fes_dens_2D.csv', sep = ' ', header = None)
    fes_2d = fes_2d.fillna(np.nanmax(fes_2d))

    d1 = pd.read_csv(f'{FOLDER}/{DATA_FOLDER}/d1.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})
    d2 = pd.read_csv(f'{FOLDER}/{DATA_FOLDER}/d2.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})

    with open(f'{FOLDER}/{DATA_FOLDER}/data.txt', 'w') as f: 
        for i in range(fes_2d.shape[1]): 
            for j in range(fes_2d.shape[0]): 
                #print(i, j, d1.shape, d2.shape, fes_2d.shape)
                f.write(f"{d1['d'].iloc[i]} {d2['d'].iloc[j]} {fes_2d[i][j]}\n")
                
    return (d1, d2, fes_2d)
