#2014 Dec 3 -- Making plots of orbital evolution for some select cases
#

import mesa_reader as ms
import pylab as pl
import math
import numpy as np
from itertools import cycle
from astropy import constants as cst
import glob

#dir_names = ['Mpinit_0.5_MJup', 'Mpinit_1.0_MJup', 'Mpinit_3.0_MJup', 'Mpinit_10.0_MJup']
#dir_names = ['Mpinit_0.6_MJup_qs5', 'Mpinit_1.0_MJup_qs5', 'Mpinit_5.0_MJup_qs5', 'Mpinit_10.0_MJup_qs5']
#dir_names = ['Mpinit_0.6_MJup_qs5', 'Mpinit_1.0_MJup_qs5']
#dir_names = ['Mpinit_1.0_MJup_qs7']
#dir_names = ['Mpinit_9.9_MJup_qs7_implicit-3_P3d']
#dir_names = glob.glob('models/*qs5*')

#core_masses = ['1', '3', '5', '10', '30', '50']
core_masses = ['1', '10']

#line_names = dir_names

pl.figure(figsize=(8,6))

ax1 = pl.subplot(111)
ax1.set_xlabel('$t$ (yrs)', fontsize=24)
ax1.set_ylabel('$P$ (days)', color='b', fontsize=24)

ax2 = ax1.twinx()
ax2.set_ylabel('$M_\mathrm{p}$ ($M_\mathrm{Jup}$)', color='r', fontsize=24)
#ax2.set_ylabel('$R_\mathrm{p}$ ($R_\mathrm{Jup}$)', color='r')

#core mass (10 MEarth) in Jupiter masses
core_mass = 10.*cst.M_earth.value/cst.M_jup.value
Msol_to_MJup = cst.M_sun.value/cst.M_jup.value
hrs_to_days = 24.
yrs_to_days = 365.25

#Have lines cycle through styles rather than colors
linecycler = cycle(["-","--","-.",":"])

lines = []
line_names = []

for current_core_mass in core_masses:
#for current_dir in dir_names:
#for current_dir in [dir_names[0], dir_names[1], dir_names[2]]:

  current_dir = (glob.glob("models/*"+current_core_mass+"*_ME_qs5"))[0]
  line_names.extend([current_core_mass])

  ls = next(linecycler)

  hst = ms.history_data(current_dir, slname='binary_history.data')
# pl_density = cst.M_sun.to('g').value/(cst.R_sun.to('cm').value)**3.*\
#   hst.get('star_1_mass')/\
#   (4.*math.pi/3*(hst.get('star_1_radius'))**3)
# st_density = cst.M_sun.to('g').value/(cst.R_sun.to('cm').value)**3.*\
#   hst.get('star_2_mass')/\
#   (4.*math.pi/3*(hst.get('star_2_radius'))**3)

# pl_PRL = \
#   np.sqrt((2.44*hst.get('star_2_radius')*(st_density/pl_density)**(1./3)*\
#           cst.R_sun.value/cst.au.value)**3./hst.get('star_2_mass'))*\
#   yrs_to_days
# st_PRL = \
#   np.sqrt((2.44*hst.get('star_1_radius')*(pl_density/st_density)**(1./3)*\
#           cst.R_sun.value/cst.au.value)**3./hst.get('star_2_mass'))*\
#   yrs_to_days

  lines.extend(ax1.semilogx(hst.get('age'), hst.get('period_days'),ls=ls,color='b',lw=3))
# lines.extend(ax1.semilogx(hst.get('age'), hst.get('period_days'),ls=ls,color='b',lw=0))

# ax2.semilogx(hst.get('age'), hst.get('star_1_mass')*Msol_to_MJup,ls=ls,color='r', lw=2)
  ax2.loglog(hst.get('age'), hst.get('star_1_mass')*Msol_to_MJup,ls=ls,color='r', lw=3)
# ax2.semilogx(hst.get('age'), hst.get('star_1_radius')*cst.R_sun.value/cst.R_jup.value,ls=ls,color='r', lw=2)

#ax1.plot(hst.get('age'), np.sqrt((hst.get('star_2_radius')*cst.R_sun.value/cst.au.value)**3./(hst.get('star_2_mass')))*yrs_to_days, lw=3, color='black')
#ax1.fill_between(hst.get('age'), np.sqrt((hst.get('star_2_radius')*cst.R_sun.value/cst.au.value)**3./(hst.get('star_2_mass')))*yrs_to_days, color='blue')

#ax2.plot(hst.get('age'), np.repeat(core_mass, len(hst.get('age'))), lw=3, color='black')
#ax2.fill_between(hst.get('age'), core_mass, y2=1e-2, color='red', alpha=0.5)

for tl in ax1.get_yticklabels():
    tl.set_color('b')
for tl in ax2.get_yticklabels():
    tl.set_color('r')

ax1.set_xlim([3e6, 2e10])
ax2.set_ylim([1e-2, 2e1])

handles, labels = ax1.get_legend_handles_labels()
#line_names[0] = '$M_\mathrm{core} =\ 5\ M_\mathrm{Earth}$'
line_names[0] = '$M_\mathrm{core} =\ 1\ M_\mathrm{Earth}$'
line_names[1] = '$10\ M_\mathrm{Earth}$'
#line_names[2] = '$50\ M_\mathrm{Earth}$'

#ax2.text(3e6, 1.25*core_mass, '$M_\mathrm{p} = M_\mathrm{core}\ (10\ M_\mathrm{Earth})$', color='black', fontsize=18)

leg = ax1.legend(lines, line_names, labelspacing=0.1, loc='lower left', fontsize=24)
leg.draw_frame(False)
# set the line color of each legend object
for legobj in leg.legendHandles:
    legobj.set_color('black')

ax1.text(5e6, 1, "$M_{\\rm p, 0} = 1\ M_{\\rm Jup}$", fontsize=24)

pl.show()
#pl.savefig('/Users/bjackson/research/superpig/RLO/plot_orbital_mass_evolution_variable-core.png',bbox_inches='tight')
#pl.savefig('/Users/bjackson/research/superpig/RLO/plot_orbital_mass_evolution_variable-core_abbrev.png',bbox_inches='tight')
#pl.savefig('plot_orbital_mass_evolution_variable-core_2015May21.png',bbox_inches='tight', dpi=500)
