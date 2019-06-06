#2014 Dec 8 -- Makes age contour plot in Rp-Mp space
# XXX for comparison to Fortney+ (2007) Fig 8 XXX
# for comparison to Paxton+ (2013) Fig 3

import mesa as ms
import pylab as plt
import math
import numpy as np
import glob
from scipy.interpolate import griddata

MJup_to_Msol = 1.898e27/1.9891e30
MJup_to_MEarth = 318.
RJup_to_Rsol = 69911./6.955e5

age = []
radius = []
mass = []

'''
dirs = glob.glob('models/Mpinit*')[::-1]
for current_dir in dirs:
  a1 = ms.history_data(sldir=current_dir+'/LOGS1', slname='history.data')
  temp_entropy = a1.get('center_entropy')

# for cur_file in files:
  a1 = ms.history_data(sldir=current_dir, slname='binary_history.data')
  temp_age = a1.get('age')
  temp_radius = a1.get('star_1_radius')
  temp_mass = a1.get('star_1_mass')

  if((len(temp_radius) == len(temp_entropy)) and \
     (temp_mass.all() > 0.)):
    age.extend(temp_age)
    radius.extend(temp_radius)
    mass.extend(temp_mass)

with file('Rp_vs_Mp_4p5Gyrs.bin', 'wb') as f:
  np.save(f, age)
  np.save(f, radius)
  np.save(f, mass)
'''

with file('Rp_vs_Mp_4p5Gyrs.bin', 'rb') as f:
  age = np.load(f)
  radius = np.load(f)
  mass = np.load(f)

#convert to Jupiter masses
#x = [mass[i]/MJup_to_Msol*MJup_to_MEarth for i in range(len(mass))]
x = [mass[i]/MJup_to_Msol for i in range(len(mass))]
y = [radius[i]/RJup_to_Rsol for i in range(len(radius))]
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
CS = plt.contour(xi,yi,zi,levels=[0.001, 0.01, 0.1, 1., 10.]) 
plt.clabel(CS, inline=1, fontsize=10, cmap=plt.cm.jet)
ax.set_xscale('log')
plt.xlim(0.1, 35)
plt.ylim(0.8, 2.5)

#plt.xlim(10, 3000)
#plt.ylim(0., 1.5)

#CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
#plt.colorbar() # draw colorbar
# plot data points.
#plt.scatter(x,y,marker='o',c='b',s=5)
#plt.title('griddata test (%d points)' % npts)
plt.show()
