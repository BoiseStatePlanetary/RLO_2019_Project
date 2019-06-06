#2014 Nov 19 -- Orbital/mass evolution of Jupiter-mass planet

import mesa as ms
import pylab as pl
import numpy as np
from matplotlib.ticker import MaxNLocator 
from astropy import constants

#a1 = ms.history_data(sldir='LOGS1', slname='history.data')
#pl.semilogx(a1.get('star_age'), a1.get('radius_cm')/RJup_to_cm)

fig, ax1 = pl.subplots()
#fig.suptitle('research/superpig/RLO/mesa/tidal_evol_Jupiter')

hst = ms.history_data(sldir='.', slname='binary_history.data')

#Calculate orbital period of stellar surface
Rsun_to_AU = 5e-3
years_to_days = 365.25
Ms = hst.get('star_2_mass')
Rs = hst.get('star_2_radius')
P_stellar_surf = np.sqrt((Rs*Rsun_to_AU)**3./Ms)*years_to_days
print(P_stellar_surf)
exit()

ax1.semilogx(hst.get('age'), hst.get('period_days'), 'b')
ax1.semilogx(hst.get('age'), P_stellar_surf, 'b--', lw=2)
ax1.set_xlim([1e8, 1e10])
ax1.set_ylim([0., 3.0])
ax1.set_xlabel('$t$ (yrs)')
ax1.set_ylabel('$P$ (days)', color='b')
for tl in ax1.get_yticklabels():
  tl.set_color('b')
ax1.set_yticks(np.arange(0.5, 3.5, 0.5))
nbins = len(ax1.get_xticklabels())
#Have to do twice for some reason
#ax1.yaxis.set_major_locator(MaxNLocator(nbins=nbins, prune='lower'))

ax2 = ax1.twinx()
ax2.semilogx(hst.get('age'), hst.get('star_1_mass')*1e3, 'r')
ax2.set_xlim([1e8, 1e10])
ax2.set_ylabel('$M_\mathrm{p}$ ($M_\mathrm{Jup}$)', color='r')
for tl in ax2.get_yticklabels():
  tl.set_color('r')
ax2.yaxis.set_major_locator(MaxNLocator(nbins=nbins, prune='lower'))

ax1.annotate('$M_\mathrm{core} = 10\ M_\mathrm{Earth}$', xy=(3e9, 2.8), xytext=(1.3e9, 2.5), fontsize=24)
ax1.annotate('$R_\star$', xy=(1e8, min(P_stellar_surf)), xytext=(1.3e8, min(P_stellar_surf)*3.), fontsize=24, color='b')

pl.show()
#fig.savefig('plot_tidal_evol_Jupiter.png', bbox_inches='tight')
