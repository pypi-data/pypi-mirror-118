# julian.garcia.fernandez2@usc.es 
# last modified: 6/Sep/2021
"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
special_cases.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module includes the routines to extract the mean workfunction if MGG variability and # of dopants if RD variability is applied.

Example
-------
TODO
"""

import glob
import re
import numpy as np 

def extract_meanWF_numberdopants(path,store_path,var,param):
    """
    Methods 
    -------
    extract_meanWF_numberdopants(path,store_path,var,param):
        Function to extract mean workfunction if MGG and # of dopants if RD
        Output: 
        mean_wf_param.dat: File with two columns, #Sim_id #Mean_WF[eV] if MGG variability is applied
        number_of_dopants.dat: File with two columns, #Sim_id #Number of dopants if RD variability is applied
        
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
    
    Return
    ------
    mean_wf_param.dat: file
        file with two columns, #Sim_id #Mean_WF[eV] if MGG variability is applied
    number_of_dopants.dat: file
        file with two columns, #Sim_id #Number of dopants if RD variability is applied
	"""
    store_path_wf = f'{store_path}/mean_wf_{param}.dat'
    store_path_rd = f'{store_path}/Number_of_dopants.dat'
    path_z4 = glob.glob(f'{path}/**/z4.out', recursive= True)
    path_z4 = sorted(path_z4)
    sim_id = []
    wf = []
    rd = []
    # List of Simulation ID
    for i in range(len(path_z4)):
        directorio = path_z4[i].split(sep='/')
        voltages = path_z4[i].split(sep='/')[-1]
        sim_id.append(directorio[-2]) 
    # SPECIAL CASES
    # MGG activate, mean WF
    if var == 'MGG':
        for i in range(len(path_z4)):
            f = open(path_z4[i], "r")
            z4 = f.read()
            wf_temp = re.findall(r" Mean WF value[ =]*([\d+.e]*)[\w+, ]*rank=[\d+]*",z4)
            # print(i,path_z4[i],wf_temp)
            if len(wf_temp) > 1:
                wf_list = round((np.float64(wf_temp[0])+np.float64(wf_temp[1]))/len(wf_temp),3)
            else:
                wf_list = round(np.float(wf_temp[0]),3)
            wf.append(wf_list)
            f.close()
    # Save data on store_path
        f = open(store_path_wf, "w")
        f.write(f'''#Sim_id\t#Mean WF[eV]
FoM extracted with:\t#MGG variability
''')
        for i in range(len(sim_id)):
            f.write(f'''{sim_id[i]}\t{wf[i]}
''')
        f.close()
        return f
    # RD activate, number of dopantsvar == 'RD':
    elif var == 'RD':
        for i in range(len(path_z4)):
            f = open(path_z4[i], "r")
            z4 = f.read()
            number_dopants = np.float64(re.findall(r"Contador dopantes totales: ([\d+.e]*)",z4))
            rd.append(np.float64(number_dopants))
            f.close()
    # Save data on store_path
        f = open(store_path_rd, "w")
        f.write(f'''#Sim_id\t#Number of dopants
#FoM extracted with:\t#RD variability
''')
        for i in range(len(sim_id)):
            f.write(f'''{sim_id[i]}\t{rd[i]}
''')
        f.close()
        return f
    else:
        message = "Not number_of_dopants.dat file cause RD variability is not applied"
        return message