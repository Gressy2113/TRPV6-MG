import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import os

matplotlib.rcParams['svg.fonttype'] = 'none'

import warnings
warnings.filterwarnings("ignore")
import scipy.ndimage

from SCRIPTS.constants import *
from SCRIPTS.func_main import *

def plot_2D_L_CN(axis, FOLDER, COLVAR, 
                 dist1, dist2, cn, fes, 
                 Nbins_D1, Nbins_D2, Nbins_CN, Bonds_D1, Bonds_D2, Bonds_CN, 
                 FIG_FOLDER = 'Reweighting_images'
                 ):
    
    Ubias = -fes * (1-1/BIASF)

    WEIGHTS, ED = np.histogramdd(COLVAR[['cn', 'd_580', 'd_489']].to_numpy(), 
                                bins = [Nbins_CN, Nbins_D2, Nbins_D1],
                                range = (Bonds_CN, Bonds_D2, Bonds_D1),
                                density=True, 
                                )
    weighted_avg = np.sum(np.exp(1/kBT * Ubias) * WEIGHTS, axis=axis)
    weighted_avg[weighted_avg==0]=np.nan
    norm = np.sum(np.exp(1/kBT * (Ubias-np.max(Ubias))))
    fes_dens = -kBT * np.log(weighted_avg/norm)
    
    fes_dens = scipy.ndimage.gaussian_filter(fes_dens, 0.1)

    vmax = np.nanmax(fes_dens)//10 * 10

    if axis == 1: 
        d = dist1[0, 0, :]
    else: 
        d = dist2[0, :, 0]
    h = plt.contourf(d, cn[:, 0, 0], fes_dens, 
                cmap = 'jet', 
                origin = 'lower',
               levels = np.arange(0, vmax, 1), 
                )

    plt.contour(d, cn[:, 0, 0], fes_dens, 
                colors = 'k', 
                linewidths=0.5,
               levels = np.arange(0, vmax, 5)
                )
    plt.colorbar(h, label="Free energy, kJ/mol")
    plt.xlabel(f'L{axis}, nm')
    plt.ylabel("CN")
    plt.title(f'{FOLDER} L{axis}')
    
    plt.xlim(0., 2)#1.5)
    
    if not os.path.exists(f'{FOLDER}/{FIG_FOLDER}'):
        os.mkdir(f'{FOLDER}/{FIG_FOLDER}')

    
    plt.savefig(f'{FOLDER}/{FIG_FOLDER}/reweighting_2D_CN_{axis}.svg', dpi=300, bbox_inches = 'tight')

    plt.show()


def plot_2D_L12(FOLDER, PROF_FOLDER, PROF_NAME, PROF_NPTS, PROF_STEPMAX, IMAGE_FOLDER, color):    
    d1 = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/d1.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})
    d2 = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/d2.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})
    fes_2d = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/fes_dens_2D.csv', sep = ' ', header = None)
    
    vmax = np.max(fes_2d)//10 * 10
    h = plt.contourf(d1['d'], d2['d'], fes_2d, 
                cmap = 'jet', 
                origin = 'lower',
                aspect = 'equal',
                levels = np.arange(0, vmax, 1), 
                )

    plt.contour(d1['d'], d2['d'], fes_2d, 
                colors = 'k', 
                linewidths=0.5,
                levels = np.arange(0, vmax, 5)
                )
    if PROF_FOLDER: 
        path = np.loadtxt(f'{FOLDER}/{PROF_FOLDER}/{PROF_NAME}_pts_npts{PROF_NPTS}_stepmax{PROF_STEPMAX}.csv')
        plt.plot(path[:, 0], path[:, 1],  '-', color = 'k')
    plt.colorbar(h, label = 'FES, kJ/mol')
    plt.xlim(0.2, 1.5)
    plt.ylim(0.2, 1.5)
    plt.xlabel('L1, nm')
    plt.ylabel('L2, nm')
    plt.title(FOLDER)
    plt.savefig(f'{FOLDER}/{IMAGE_FOLDER}/reweighting_2D_L1_L2.svg', dpi=300, bbox_inches = 'tight')
    plt.show()
    
    if PROF_FOLDER: 
        prof = np.loadtxt(f'{FOLDER}/{PROF_FOLDER}/{PROF_NAME}_prof_path_npts{PROF_NPTS}_stepmax{PROF_STEPMAX}.csv')
        _plot_prof(prof, color = color, ylim = (-35, 25))
        plt.savefig(f'{FOLDER}/{IMAGE_FOLDER}/reweighting_path_1d.svg', dpi=300, bbox_inches = 'tight')
        plt.show()


def _plot_prof(prof, color, xlim = (0, 1), ylim = (-30, 15)):
    fig, ax = plt.subplots(figsize = (5.5, 3))

    reaction = np.linspace(0, 1, len(prof))
    prof -= prof[0]
    prof = prof[::-1]
    plt.plot(reaction, prof, '.-', color = color,
             markeredgecolor = 'k', 
             markeredgewidth = 0.5
             )
    ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(0, 1.1, 0.1)))
    ax.xaxis.set_minor_locator(matplotlib.ticker.FixedLocator(np.arange(0, 1.1, 0.05)))

    ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(-50, 50, 10)))
    ax.yaxis.set_minor_locator(matplotlib.ticker.FixedLocator(np.arange(-50, 50, 5)))


    plt.grid(True, which='major', linestyle=  '-')
    plt.grid(True, which='minor', linestyle=  '-', lw=0.2)
    plt.ylim(ylim)
    plt.xlim(xlim)
    ax.set_ylabel("Free energy, kJ/mol")
    ax.set_xlabel("Reaction progress")


def plot_1D_L(FOLDER, PROF_FOLDER, IMAGE_FOLDER):
    
    d1 = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/d1.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})
    d2 = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/d2.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})
    
    fig, ax = plt.subplots(figsize = (5.5, 3))
    _, _, _, dG1 = dG_calc(d1['d'], d1['G'], FOLDER)
    _, _, _, dG2 = dG_calc(d2['d'], d2['G'], FOLDER)
    print(dG1, dG2)
    plt.plot(d1['d'], d1['G'], '.-', label = 'D489', color = 'blue', 
             markeredgecolor = 'k', 
             markeredgewidth = 0.5
             )
    plt.plot(d2['d'], d2['G'], '.-', label = 'D580', color = 'tab:orange', 
             markeredgecolor = 'k', 
             markeredgewidth = 0.5
             )

    plt.ylim(-25, 20)
    ax.grid(True, which='major', linestyle=  '-')
    ax.grid(True, which='minor', linestyle=  '-', lw=0.2)
    ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(-100, 45, 10)))
    ax.yaxis.set_minor_locator(matplotlib.ticker.FixedLocator(np.arange(-100, 45, 10/4)))

    ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(0, 3, 0.5)))
    ax.xaxis.set_minor_locator(matplotlib.ticker.FixedLocator(np.arange(0, 3, 0.1)))

    plt.xlim(0, 2)#, 1.5)
    plt.title(FOLDER)
    plt.legend()
    plt.xlabel('L, nm')
    plt.ylabel('Free Energy, kJ/mol')
    plt.savefig(f'{FOLDER}/{IMAGE_FOLDER}/reweighting_1D_L.svg', dpi=300, bbox_inches = 'tight')
    plt.show()
    
    
def plot_2D_ace(FOLDER, PROF_FOLDER = 'Reweighting_data', IMAGE_FOLDER = 'Reweighting_images'): 
    
    if not os.path.exists(f'{FOLDER}/{IMAGE_FOLDER}'):
        os.mkdir(f'{FOLDER}/{IMAGE_FOLDER}')

    FES_1D = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/prof_1D.csv', sep = ' ', header = None).rename(columns={0:'d', 1:'G'})
    CN = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/cn.csv', sep = ' ', header = None).rename(columns={0:'cn'})
    FES_2D = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/fes_dens_2D.csv', sep = ' ', header = None)
    
    fig, ax = plt.subplots()
    ax.set_box_aspect(1)
    vmax = np.nanmax(FES_2D)//10 * 10
    h = plt.contourf(FES_1D['d'], CN['cn'], FES_2D.T, 
                cmap = 'jet', 
                origin = 'lower',
                levels = np.arange(0, vmax, 1), 
                )

    plt.contour(FES_1D['d'], CN['cn'], FES_2D.T, 
                colors = 'k', 
                linewidths=0.5,
                levels = np.arange(0, vmax, 10)
                )
    
    plt.xlim(0., 2)
    
    plt.colorbar(h, label="Free energy, kJ/mol")
    plt.xlabel('L, nm')
    plt.ylabel("CN")
    plt.title(FOLDER)
    plt.savefig(f'{FOLDER}/{IMAGE_FOLDER}/FES_2D_reweighting.svg', dpi=300, bbox_inches = 'tight')
    plt.show()


def plot_1D_ace(FOLDER, PROF_FOLDER, fig, ax, color):
    
    FES_1D = pd.read_csv(f'{FOLDER}/{PROF_FOLDER}/prof_1D.csv', sep = ' ', header = None).rename(columns={0:'d', 1:'G'})
    
    _, _, _, dG = dG_calc(FES_1D['d'], FES_1D['G'], FOLDER)
    
    if ax is None: 
        fig, ax = plt.subplots(figsize = (5.5, 3))
    plt.plot(FES_1D['d'], FES_1D['G'], '.-', lw = 1, color = color, label = FOLDER.split('/')[1])
    plt.ylim(-15, 20)
    plt.xlim(0., 2)


    ax.grid(True, which='major', linestyle=  '-')
    ax.grid(True, which='minor', linestyle=  '-', lw=0.2)
    ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(-100, 45, 10)))
    ax.yaxis.set_minor_locator(matplotlib.ticker.FixedLocator(np.arange(-100, 45, 10/4)))

    ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(np.arange(0, 3, 0.5)))
    ax.xaxis.set_minor_locator(matplotlib.ticker.FixedLocator(np.arange(0, 3, 0.1)))

    plt.xlabel('L, nm')
    plt.ylabel('Free Energy, kJ/mol')

    
