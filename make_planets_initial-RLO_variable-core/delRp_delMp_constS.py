#2014 Dec 8 -- Makes entropy contour plot in Rp-Mp space

import mesa as ms
import pylab as plt
import math
import numpy as np
import glob
from scipy.interpolate import griddata

MJup_to_Msol = 1.898e27/1.9891e30
RJup_to_Rsol = 69911./6.955e5

center_entropy = []
radius = []
mass = []

dirs = glob.glob('models/Mpinit*')[::-1]
'''
for current_dir in dirs:
  a1 = ms.history_data(sldir=current_dir+'/LOGS1', slname='history.data')
  temp_entropy = a1.get('center_entropy')

# for cur_file in files:
  a1 = ms.history_data(sldir=current_dir, slname='binary_history.data')
  age = a1.get('age')
  temp_radius = a1.get('star_1_radius')
  temp_mass = a1.get('star_1_mass')

  if((len(temp_radius) == len(temp_entropy)) and \
     (temp_mass.all() > 0.)):
    center_entropy.extend(temp_entropy)
    radius.extend(temp_radius)
    mass.extend(temp_mass)

with file('delRp_delMp_constS.bin', 'w') as f:
  np.save(f, center_entropy)
  np.save(f, radius)
  np.save(f, mass)
'''

with file('delRp_delMp_constS.bin', 'r') as f:
  center_entropy = np.load(f)
  radius = np.load(f)
  mass = np.load(f)

#convert to Jupiter masses
x = [mass[i]/MJup_to_Msol for i in range(len(mass))]
y = [radius[i]/RJup_to_Rsol for i in range(len(radius))]
z = center_entropy
npts = 100
del_x = (max(x) - min(x))/(npts - 1.)
xi = np.linspace(min(x), max(x) + del_x, npts)
del_y = (max(y) - min(y))/(npts - 1.)
yi = np.linspace(min(y), max(y) + del_y, npts)
# grid the data.
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='linear')

fig = plt.figure()
ax = fig.add_subplot(111)
CS = plt.contour(xi,yi,zi,range(7,12))
plt.clabel(CS, inline=1, fontsize=10, cmap=plt.cm.jet)
ax.set_xscale('log')
plt.xlim(0.1, 11)
plt.ylim(0.8, 2.5)

#CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
#plt.colorbar() # draw colorbar
# plot data points.
#plt.scatter(x,y,marker='o',c='b',s=5)
#plt.title('griddata test (%d points)' % npts)
plt.show()
