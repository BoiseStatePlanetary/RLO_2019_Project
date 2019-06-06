#2014 Nov 29 -- Run RLO calculation for initial grid of masses

import update_inlist as ul
import numpy as np
import os
from os.path import isfile
from os.path import isdir
import glob

from astropy import constants as const

import shutil

yrs_to_days = 365.25

def check_make_file(template_file_name, current_mass, core_mass, dir_name):

  inlist_file_name = dir_name+'/'+template_file_name.replace('template', str(current_mass)+'_MJ_3.0_RJ_'+str(core_mass)+'_ME')
  if(not isfile(inlist_file_name)):
    shutil.copy2(template_file_name, inlist_file_name)

  return inlist_file_name

def TRL(Ms=1.0, Mp=1.0, Rs=1.0, Rp=1.0, Qs=1e7, a0=0.02):
  #Ms/Rs in solar, Mp/Rp in Jupiter, a0 in AU

  #Roche limit for Jupiter around the Sun
  aRL = 0.012
  
  #timescale, in years
  TRL0 = 8.4e6

  return Ms**(8./3)*Mp**(-19./6)*Rs**(-5.)*Rp**(13./2)*(Qs/1e7)*\
         ((a0/aRL)**(13./2)-1.)*TRL0

def a0(Ms=1.0, Mp=1.0, Rs=1.0, Rp=1.0, Qs=1e7, TRL=8.4e6):
  #Calculate a0 such that TRL is given value
  #
  #Ms/Rs in solar, Mp/Rp in Jupiter, a0 in AU

  #Roche limit for Jupiter around the Sun
  aRL = 0.012
  
  #timescale, in years
  TRL0 = 8.4e6

  return ((TRL/TRL0)*\
          Ms**(-8./3)*Mp**(19./6)*Rs**(5.)*Rp**(-13./2)*(1e7/Qs)+1.)**(2./13)*\
          aRL

def P0(Ms=1.0, Mp=1.0, Rs=1.0, Rp=1.0, Qs=1e7, TRL=8.4e6):
  #Calculate a0 such that TRL is given value
  #
  #Ms/Rs in solar, Mp/Rp in Jupiter, a0 in AU

  #Roche limit for Jupiter around the Sun
  aRL = 0.012
  
  #timescale, in years
  TRL0 = 8.4e6
  
  init_a = a0(Ms=Ms, Mp=Mp, Rs=Rs, Rp=Rp, Qs=Qs, TRL=TRL)

  return np.sqrt(init_a**3/Ms)*yrs_to_days

#generate array of masses in reverse order so that models that are likely
#  to cause problems are run last
#file_list = (glob.glob('../make_planets_initial-grid/models/*/*evolve*.mod'))[::-1]

#2014 Dec 5 -- 10 Mearth cores
file_list = (glob.glob('../make_planets_initial-grid_variable-core/models/*/*evolve*.mod'))[::-1]
print(file_list)

original_inlist_file_name = 'original_inlist_project'
final_inlist_file_name = 'inlist_project'

for current_file in [file_list[0]]:

  lst = current_file.split('/')
# print("You've taken qs = 5, P = 3 day!!")

  #2014 Dec 27 -- Retrieve initial mass
  olst = lst[3].split('_')
  cur_mass = float(olst[1])
  cur_core_mass = float(olst[3])

# dir_name = 'models/' + lst[3] + '_qs5'
  dir_name = 'models/' + lst[3] + '_qs7'
  if(not isdir(dir_name)):
    os.mkdir(dir_name)

  #shutil.copy2(current_file, 'planet_init.mod')
  os.system("cp " + current_file + " planet_init.mod")

  #clean up
  os.system("./mk > /dev/null")
  os.chmod('star_binary', 0770)
  os.chmod('rn', 0770)

  #run the calculation
# os.system("./rn >> make_planets_initial-RLO_10Mearth_log.txt")
  os.system("./rn")

  #move LOGS
  os.system("cp -r LOGS1 " + dir_name)
  os.system("cp -r LOGS2 " + dir_name)
  os.system("cp -r photos1 " + dir_name)
  os.system("cp -r photos2 " + dir_name)
  os.system("cp binary_history.data " + dir_name)

  #clean up
  os.system("./clean")

  print("***")
  
