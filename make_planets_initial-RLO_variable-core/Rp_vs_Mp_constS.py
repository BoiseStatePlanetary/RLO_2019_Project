#2014 Dec 8 -- Makes entropy contour plot in Rp-Mp space

import mesa as ms
import pylab as plt
import math
import numpy as np
import glob
from scipy.interpolate import griddata
import os

MJup_to_Msol = 1.898e27/1.9891e30
RJup_to_Rsol = 69911./6.955e5
RJup_to_cm = 7.1492e9 #from Paxton+ (2013)

age = []
center_entropy = []
radius = []
mass = []

#dirs = glob.glob('models/Mpinit*')[::-1]
dirs = glob.glob('models/Mpinit*MJup_qs5/')[::-1]
#'''
for current_dir in dirs:
# os.system('rm '+current_dir+'/LOGS1/history.datasa')
  a1 = ms.history_data(sldir=current_dir+'/LOGS1/', slname='history.data')
  temp_entropy = a1.get('center_entropy')

# for cur_file in files:
# a1 = ms.history_data(sldir=current_dir, slname='binary_history.data')
  temp_age = a1.get('star_age')
  temp_radius = a1.get('radius_cm')/RJup_to_cm
  temp_mass = a1.get('star_mass')/MJup_to_Msol

  if((len(temp_radius) == len(temp_entropy)) and \
     (temp_mass.all() > 0.)):
    age.extend(temp_age)
    center_entropy.extend(temp_entropy)
    radius.extend(temp_radius)
    mass.extend(temp_mass)

with file('Rp_vs_Mp_constS.bin', 'wb') as f:
  np.save(f, age)
  np.save(f, center_entropy)
  np.save(f, radius)
  np.save(f, mass)
#'''

with file('Rp_vs_Mp_constS.bin', 'rb') as f:
  age = np.load(f)
  center_entropy = np.load(f)
  radius = np.load(f)
  mass = np.load(f)

#convert to Jupiter masses
#x = [mass[i]/MJup_to_Msol for i in range(len(mass))]
#y = [radius[i]/RJup_to_Rsol for i in range(len(radius))]
x = mass
y = radius
#z = center_entropy
z = age/1e9
npts = 100
del_x = (max(x) - min(x))/(npts - 1.)
xi = np.linspace(min(x), max(x) + del_x, npts)
del_y = (max(y) - min(y))/(npts - 1.)
yi = np.linspace(min(y), max(y) + del_y, npts)
# grid the data.
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='linear')

fig = plt.figure()
ax = fig.add_subplot(111)
#CS = plt.contour(xi,yi,zi,range(7,12),linewidths=3)
CS = plt.contour(xi,yi,zi,[0.01, 0.1, 1],linewidths=3)
plt.clabel(CS, inline=1, fontsize=18, cmap=plt.cm.jet, fmt='%i')
ax.set_xscale('log')
plt.xlim(0.1, 11)
plt.ylim(0.8, 2.5)

plt.xlabel("$M_\mathrm{p}\ (M_\mathrm{Jup})$")
plt.ylabel("$R_\mathrm{p}\ (R_\mathrm{Jup})$")

#CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
#plt.colorbar() # draw colorbar
# plot data points.
#plt.scatter(x,y,marker='o',c='b',s=5)
#plt.title('griddata test (%d points)' % npts)
plt.text(2, 2.3, '$R_\mathrm{p, init} = 3\ R_\mathrm{Jup}$', fontsize=24)
plt.show()
#plt.savefig('/Users/bjackson/research/superpig/RLO/Rp_vs_Mp_constS_no-core.png', bbox_inches='tight')
