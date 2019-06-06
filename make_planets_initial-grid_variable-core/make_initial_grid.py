#2014 Nov 23 -- Make evolution grid spanning masses from 0.1 to 10 MJup

import update_inlist as ul
import numpy as np
import os
from os.path import isfile
from os.path import isdir
from astropy import constants as cst

import shutil

def check_make_file(template_file_name, current_mass, core_mass, dir_name):

  inlist_file_name = dir_name+'/'+template_file_name.replace('template', str(current_mass)+'_MJ_3.0_RJ_'+str(core_mass)+'_ME')
  if(not isfile(inlist_file_name)):
    shutil.copy2(template_file_name, inlist_file_name)

  return inlist_file_name

#generate array of masses in reverse order so that models that are likely
#  to cause problems are run last
#masses = (np.arange(0.1, 10.1, 0.1))[::-1]
#core_masses = [1., 3., 5., 30., 50.]
core_masses = [1.]
#
#2014 Nov 27 -- For some reason, Mpinit = 0.6 MJup crashes but no other,
#  so I'm going to tweak the initial radius to see if that makes a difference.
#masses = [0.6]

#convert Jupiter mass to grams
MJup_to_g = 1.898e+30

current_mass = 1.0 #Jupiter

inlist_create_template = 'inlist_create_template'
inlist_core_template = 'inlist_core_template'
inlist_evolve_template = 'inlist_evolve_template'

original_run_file_name = 'original_rn'
run_file_name = 'rn'

for current_core_mass in core_masses:
  dir_name = 'models/Mpinit_'+str(current_mass)+'_MJup_'+str(current_core_mass)+'_ME'

  #check first whether you've made the directory
  if(not isdir(dir_name)):
    os.mkdir(dir_name)

  #write inlist files

  #Don't need to create; just copy planet_create_1.0_MJ_3.0_RJ.mod from research/mesa/mwd/make_planets_initial-grid_10Mearth/models/Mpinit_1.0_MJup

  #core file
  core_inlist_file_name = check_make_file(inlist_core_template, current_mass, current_core_mass, dir_name)
  with open(inlist_core_template, 'r') as text_file:
    final_inlist = text_file.read().split('\n')
    
  params = ['save_model_filename', 'new_core_mass']
  core_model_name = dir_name+'/'+'planet_core_'+str(current_mass)+'_MJ_3.0_RJ_'+str(current_core_mass)+'_ME.mod'
  values = ['"'+core_model_name+'"', current_core_mass*cst.M_earth.value/cst.M_sun.value]
  commands = ['modify', 'modify']
  sections = ['star_job', 'star_job']

  for param,command,value,section in zip(params,commands,values,sections):
    final_inlist = ul.update_param(final_inlist, param=param, value=value, command=command, section=section)

  with open(core_inlist_file_name, 'w') as text_file:
    text_file.write('\n'.join(final_inlist))
    text_file.write('\n')

  #evolve file
  evolve_inlist_file_name = check_make_file(inlist_evolve_template, current_mass, current_core_mass, dir_name)
  with open(inlist_evolve_template, 'r') as text_file:
    final_inlist = text_file.read().split('\n')

  params = ['saved_model_name', 'save_model_filename']
  evolve_model_name = dir_name+'/'+'planet_evolve_'+str(current_mass)+'_MJ_3.0_RJ_'+str(current_core_mass)+'_ME.mod'
  values = ['"'+core_model_name+'"', '"'+evolve_model_name+'"']
  commands = ['modify', 'modify']
  sections = ['star_job', 'star_job']

  for param,command,value,section in zip(params,commands,values,sections):
    final_inlist = ul.update_param(final_inlist, param=param, value=value, command=command, section=section)

  with open(evolve_inlist_file_name, 'w') as text_file:
    text_file.write('\n'.join(final_inlist))
    text_file.write('\n')

  #Now to modify the run file
  with open(original_run_file_name, 'r') as original_run_file:
    original_run_file_contents = original_run_file.read().split('\n')

    original_run_file_contents.\
      extend(['echo "Running Mpinit = ' + str(current_mass) + ' MJup"'])

    print('echo Running Mpinit = ' + str(current_mass) + ' MJup\n')

    #Check whether the desired model already exists before running
    if(not isfile(core_model_name)):
      print("Didn't find core file\n")
      original_run_file_contents.extend(['do_one ' + core_inlist_file_name + \
                               ' ' + core_model_name])
    if(not isfile(evolve_model_name)):
      print("Didn't find evolve file\n")
      original_run_file_contents.extend(['do_one ' + evolve_inlist_file_name + \
                               ' ' + evolve_model_name])
    original_run_file_contents.\
      extend(['date "+DATE: %Y-%m-%d%nTIME: %H:%M:%S"'])

    original_run_file_contents.\
      extend(['echo "finished all inlists for make_planets"'])

  with open(run_file_name, 'w') as run_file:
    run_file.write('\n'.join(original_run_file_contents))

  print("Running rn\n")
  os.chmod(run_file_name, 0700)
  os.system("./rn")

  print("Finished\n")
  print("***")
