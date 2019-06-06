#2014 Nov 18 -- A first try at using update_inlist

import update_inlist as ul

inlist_name = 'inlist_create_test'
#commandlist=[('max_model_number','modify',-1,'any'), ('max_years_for_timestep','modify',1e9,'any'), ('do_element_diffusion','modify','.true.','any'), ('pgstar_flag','modify','.true.','any')] 
param = 'max_model_number'
value = -1
command = 'modify'
section = 'any'

inlist = open(inlist_name, 'r').read().split('\n')
print(ul.update_param(inlist, param=param, value=value, command=command, section=section))
