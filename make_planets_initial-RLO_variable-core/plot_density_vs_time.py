#2015 Jan 1 -- Making plots of evolution of planetary radius
#

import mesa as ms
import pylab as pl
import math
import numpy as np
from itertools import cycle
from astropy import constants as cst

#dir_names = ['Mpinit_0.5_MJup', 'Mpinit_1.0_MJup', 'Mpinit_3.0_MJup', 'Mpinit_10.0_MJup']
dir_names = ['Mpinit_0.6_MJup_qs5', 'Mpinit_1.0_MJup_qs5', 'Mpinit_5.0_MJup_qs5', 'Mpinit_10.0_MJup_qs5']
#dir_names = ['Mpinit_0.6_MJup_qs5']
#dir_names = ['Mpinit_9.9_MJup_qs7_implicit-3_P3d']
#line_names = ['$M_\mathrm{p, 0}\ =\ 0.5\ M_\mathrm{Jup}$', '$1$', '$3$', '$10$']
line_names = ['$M_\mathrm{p, 0}\ =\ 0.6\ M_\mathrm{Jup}$', '$1$', '$5$', '$10$']

pl.figure(figsize=(8,6))

ax1 = pl.subplot(111)
ax1.set_xlabel('$t$ (yrs)', fontsize=18)

#ax1.set_ylabel('$R_\mathrm{p}$ ($R_\mathrm{Jup}$)', color='b')
ax1.set_ylabel('$P$ (days)', color='b', fontsize=18)

ax2 = ax1.twinx()
ax2.set_ylabel('$\\rho_\mathrm{p}$ ($\mathrm{g\ cm}^3$)', color='r', fontsize=18)

#core mass (10 MEarth) in Jupiter masses
core_mass = 10.*cst.M_earth.value/cst.M_jup.value
Msol_to_MJup = cst.M_sun.value/cst.M_jup.value
hrs_to_days = 24.
yrs_to_days = 365.25

#Have lines cycle through styles rather than colors
linecycler = cycle(["-","--","-.",":"])

lines = []

#for current_dir in dir_names:
for current_dir in dir_names:

  print(current_dir)
  ls = next(linecycler)

  hst = ms.history_data('models/'+current_dir, slname='binary_history.data')
  pl_density = cst.M_sun.to('g').value/(cst.R_sun.to('cm').value)**3.*\
    hst.get('star_1_mass')/\
    (4.*math.pi/3*(hst.get('star_1_radius'))**3)

  lines.extend(ax1.semilogx(hst.get('age'), hst.get('period_days'),ls=ls,color='b', lw=3))
  ax2.loglog(hst.get('age'), hst.get('star_1_radius')*cst.R_sun.value/cst.R_jup.value, ls=ls,color='r',lw=3)

for tl in ax1.get_yticklabels():
    tl.set_color('b')
for tl in ax2.get_yticklabels():
    tl.set_color('r')

ax1.set_xlim([3e6, 2e10])
ax2.set_ylim([1e-2, 2e1])

handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, line_names)

#ax2.text(5e9, 0.6125*core_mass, '$M_\mathrm{p} = M_\mathrm{core}\ (10\ M_\mathrm{Earth})$', color='r')

leg = ax1.legend(lines, line_names, labelspacing=0.1)
leg.draw_frame(False)
# set the line color of each legend object
for legobj in leg.legendHandles:
    legobj.set_color('black')

pl.show()
#pl.savefig('/Users/bjackson/research/superpig/RLO/plot_orbital_mass_evolution_10Mearth_R3p0.png',bbox_inches='tight')
#pl.savefig('/Users/bjackson/research/pubs/presentations/AAS 2015/plot_orbital_mass_evolution_10Mearth_M0p6.png',bbox_inches='tight')
#pl.savefig('/Users/bjackson/research/pubs/presentations/AAS 2015/plot_orbital_mass_evolution_10Mearth_M0p6-1p0.png',bbox_inches='tight')
#pl.savefig('/Users/bjackson/research/pubs/presentations/AAS 2015/plot_orbital_mass_evolution_10Mearth.png',bbox_inches='tight')
