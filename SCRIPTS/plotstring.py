
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata, interp1d
from matplotlib import cm
import sys


############################################################################
FOLDER = sys.argv[1]
npts = int(sys.argv[2])

stepmax=int(sys.argv[3])

pref=sys.argv[4]

if not os.path.exists(f'{FOLDER}/MFEP_images'):
	os.mkdir(f'{FOLDER}/MFEP_images')
DATA_FOLDER = 'Reweighting_data'

##
fes_2d = pd.read_csv(f'{FOLDER}/{DATA_FOLDER}/fes_dens_2D.csv', sep = ' ', header = None)
fes_2d = fes_2d.fillna(np.nanmax(fes_2d))

print(fes_2d.shape)
d1 = pd.read_csv(f'{FOLDER}/{DATA_FOLDER}/d1.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})
d2 = pd.read_csv(f'{FOLDER}/{DATA_FOLDER}/d2.csv', sep = ' ', header = None).T.rename(columns={0:'d', 1:'G'})
print(d1.shape, d2.shape, fes_2d.shape)
with open(f'{FOLDER}/{DATA_FOLDER}/data.txt', 'w') as f: 
	for i in range(fes_2d.shape[1]): 
		for j in range(fes_2d.shape[0]): 
			f.write(f"{d1['d'].iloc[i]} {d2['d'].iloc[j]} {fes_2d[i][j]}\n")

##
data = np.loadtxt(f"{FOLDER}/{DATA_FOLDER}/data.txt")
row_min = data[np.where(data[:, 2] == data[:, 2].min())[0][0]]
print(row_min, flush=True)



data_bulk = data[np.where(((2 > data[:,0]) & (data[:,0] > 1.5)) & ((2 > data[:, 1]) & (data[:, 1] > 1.5)))]
data_bulk
xstart, ystart =data_bulk[data_bulk[:, 2] == np.min(data_bulk[:, 2])][0][:2]

data_bulk1 = data[np.where(((1.5 > data[:,0]) & (data[:,0] > 1)) & ((1.5 > data[:, 1]) & (data[:, 1] > 1)))]
data_bulk1
xprom, yprom =data_bulk1[data_bulk1[:, 2] == np.min(data_bulk1[:, 2])][0][:2]

units = 'kJ/mol'
a=(xstart, ystart)
b =(row_min[0], row_min[1])
t=(xprom, yprom)

#############################################################################

nx=np.size(np.unique(data[:,0]))
ny=np.size(np.unique(data[:,1]))
print(nx, ny)

order = 'C'

if data[0,0] != data[1,0]:
	order = 'F'
x = data[:,0].reshape(nx,ny, order=order)
y = data[:,1].reshape(nx,ny, order=order)
z = data[:,2].reshape(nx,ny, order=order)

xdiff = np.diff(x, axis=0)
ydiff = np.diff(y, axis=1)
if (not np.all(np.abs(xdiff - xdiff[0]) < 1e-8)) or (not np.all(np.abs(ydiff - ydiff[0]) < 1e-8)):
	print("WARNING! The input data is not coming from an equally spaced grid. imshow will be subtly wrong as a result, as each pixel is assumed to represent the same area.", flush=True)

gridpoints = np.vstack([x.flatten(),y.flatten()]).T

#Make a figure and a axes
fig, ax = plt.subplots(1,1)

#Use the guessed basins to make the original string, a linear interpolation between points a, t, and b.
pts = np.vstack([np.hstack([np.linspace(a[0],t[0],npts),np.linspace(t[0],b[0],npts)]),np.hstack([np.linspace(a[1],t[1],npts),np.linspace(t[1],b[1],npts)])]).T
gradx, grady = np.gradient(z,np.unique(data[:,0]),np.unique(data[:,1]))
#Evolve points so that they respond to the gradients. This is the "zero temperature string method"
for i in range(stepmax):
	#Find gradient interpolation
	Dx = griddata(gridpoints,gradx.flatten(),(pts[:,0],pts[:,1]), method='linear')
	Dy = griddata(gridpoints,grady.flatten(),(pts[:,0],pts[:,1]), method='linear')
	h = np.amax(np.sqrt(np.square(Dx)+np.square(Dy)))
	#Evolve
	pts -= 0.01 * np.vstack([Dx,Dy]).T / h
	#Reparameterize
	arclength = np.hstack([0,np.cumsum(np.linalg.norm(pts[1:] - pts[:-1],axis=1))])
	arclength /= arclength[-1]
	pts = np.vstack([interp1d(arclength,pts[:,0])(np.linspace(0,1,2*npts)), interp1d(arclength,pts[:,1])(np.linspace(0,1,2*npts))]).T
	if i % 10 == 0:
		print(i, np.sum(griddata(gridpoints,z.flatten(),(pts[:,0],pts[:,1]), method='linear')),flush=True)
		#This draws the intermediate states to visualize how the string evolves.
		ax.plot(pts[:,0],pts[:,1], color=plt.cm.spring(i/float(stepmax)))

np.savetxt(f'{FOLDER}/{DATA_FOLDER}/{pref}_pts_npts{npts}_stepmax{stepmax}.csv', pts)

ax.plot(pts[:,0],pts[:,1], color='k', linestyle='--')

heatmap = ax.imshow(z.T, cmap=plt.cm.rainbow, vmin = np.nanmin(z), vmax=1.2 * np.nanmax(griddata(gridpoints,z.flatten(),(pts[:,0],pts[:,1]), method='linear')), origin='lower', aspect='auto', extent = (x[0][0], x[-1][-1],y[0][0], y[-1][-1]), interpolation="bicubic")
heatmap.cmap.set_over('white')
ax.autoscale(False)

bar = fig.colorbar(heatmap)
bar.set_label("Free Energy (%s)" % units, rotation=90, fontsize=14)
#bar.set_ticks([-5,0,5,10,15,20])

fig.savefig(f"{FOLDER}/MFEP_images/demo.png", dpi=300, bbox_inches = 'tight')

fig, ax = plt.subplots(1,1)
reaction, prof = np.linspace(0,1,2*npts), griddata(gridpoints,z.flatten(),(pts[:,0],pts[:,1]), method='linear')
ax.plot(reaction, prof)
np.savetxt(f'{FOLDER}/{DATA_FOLDER}/{pref}_reaction_path_npts{npts}_stepmax{stepmax}.csv', reaction)
np.savetxt(f'{FOLDER}/{DATA_FOLDER}/{pref}_prof_path_npts{npts}_stepmax{stepmax}.csv', prof)

ax.set_ylabel("Free Energy (%s)" % units)
ax.set_xlabel("Reaction Progress")
fig.savefig(f"{FOLDER}/MFEP_images/1Dpmf.png", dpi=300, bbox_inches = 'tight')

fig, ax = plt.subplots(1,1)
z1 = z - z[(x > 2) & (y > 2)].mean()
ax.plot(pts[:,0],pts[:,1], '.-', color='k',)
ax.contour(x,y, z1, 
            linewidths=0.25, colors='k')
cntr = ax.contourf(x,y,z1, 
                    cmap=cm.jet)
plt.xlim(0, 1.5)
plt.ylim(0, 1.5)
plt.colorbar(cntr, label = 'FES, kJ/mol')
plt.xlabel('D1, nm')
plt.ylabel('D2, nm')
plt.savefig(f'{FOLDER}/MFEP_images/MFEP.png', bbox_inches = 'tight', dpi=150)

exit()

