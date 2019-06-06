#2014 Sep 3 -- Experiments with mesa.pyc

import mesa as ms
import pylab as pl
import math
import numpy as np

RJup_to_cm = 7.1492e9

fig = pl.figure()
#fig.suptitle('inlist_evolve_0.1_MJ_25.0_ME_2.0_RJ_no-irrad')

#a1 = ms.history_data('LOGS/')
a1 = ms.mesa_profile('models/Mpinit_0.1_MJup/planet_evolve_0.1_MJ_3.0_RJ_10Mearth.mod')
print(vars(a1))
exit()
ax = pl.semilogx(a1.get('star_age'), a1.get('radius_cm')/RJup_to_cm)
pl.show()
pl.xlabel('$t$ (yrs)')
pl.ylabel('$R_\mathrm{p}$ ($R_\mathrm{Jup}$)')
#fig.savefig('Fortney2007_Fig5.png')
