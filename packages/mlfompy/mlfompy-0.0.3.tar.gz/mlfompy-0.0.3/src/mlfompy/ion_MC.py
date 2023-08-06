# julian.garcia.fernandez2@usc.es 
# last modified: 6/Sep/2021
"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ion_MC.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module includes the routines to extract the Ion from Monte Carlo data.

Example
-------
TODO
"""

import glob
import numpy as np
import re
import os

def ion_mc(path,store_path,var,param,ion_input):
    """
    Methods 
    -------
    ion_mc(path,store_path,var,param,ion_input):
        Function to extract Ion data from fichero_particulas (MC simulations)
        
    Parameters
    ----------
    path : path
        path of simulations
    store_path : path
        path to store the output files
    var: string
        label of the variability applied
    param: string
        variability parameter applied to the device
    ion_input: y/n
        console asks if ion MC data is avaliable

    Return
    ------
    Ion_MC_var_param.dat: file
        file with two columns, #Sim_id #Ion[A] of MC simulations
	"""
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        # PATH OF MC simulations
        store_path_ion = store_path+'Ion_MC_'+var+'_'+param+'.dat'
        # READING ALL fichero_particula files
        fichero_particula = glob.glob(path +'/**/fichero_particula_FEM.sal.00.dat.*', recursive = True)
        fichero_particula = sorted(fichero_particula)
        sim_id = []
        Ion = []
        # List of Simulation ID
        for i in range(len(fichero_particula)):
            directorio = os.path.dirname(fichero_particula[i])
            # print("MC directory",directorio)
            voltages = fichero_particula[i].split(sep='/')[-1]
            Vg, Vd = np.float64(voltages.split(sep='.')[-2])/100, np.float64(voltages.split(sep='.')[-1])/100
            sim_id.append(directorio)
        # List of Ion values for each simulation
        for i in range(len(sim_id)):
            f = open(fichero_particula[i], 'r')
            line_list = f.readlines()
            empty_files = os.stat(fichero_particula[i]).st_size == 0
            if empty_files == True:
                Ion.append('NA')
            else:
                last_line = line_list[len(line_list)-1]
            if last_line.split(sep=' ')[0] != '1.500000e+03':
                Ion.append('NA')
            else:
                Ion.append(np.format_float_scientific(abs(np.float64(last_line.split(sep=' ')[-9])),4))
            f.close()
            # Save data on store_path
            f = open(store_path_ion, "w+")
            f.write(f'''#Sim_id\t#Ion[A]
#FoM extracted with:\t#Vg_on={Vg}V
''')
        for i in range(len(sim_id)):
            f.write(f'''{sim_id[i]}\t{Ion[i]}
''')
        f.close()
        return f, ion_input
    else:
        return ion_input