# julian.garcia.fernandez2@usc.es
# last modified: 6/Sep/2021
"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
build_dataset.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module includes the routines to build the dataset and make the statistics of the FoMs extracted.

Example
-------
TODO
"""

import pandas as pd 
import numpy as np
import glob
import re
import os

def build_dataset(path,path_device,var,param,Ps,ion_input):
    """
    Methods 
    -------
    build_dataset(path,path_device,var,param,Ps,ion_input=None):
        Function to build the FoM datasets
        
    Parameters
    ----------
    path: path
        path of simulations
    path_device: path
        path of the device simulations
    var: string
        label of the variability applied
    param: string
        variability parameter applied to the device
    Ps: float
        semiconductor perimeter to normalize current
    ion_input: y/n
        console asks if ion MC data is avaliable
    QC: string
        quantum corrections

    Return
    ------
    DF_var_param.dat: file
        dataset with FoM at a concrete var and param
    Statistics_var_param.dat: file
        file with the statistics of the FoMs
	"""
    # Open and read z4.out
    store_path = f'{path_device}/Datasets/{var}/DF_{var}_{param}.dat'
    dataset_dir = os.path.dirname(store_path)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        print("Dataset directory created:", dataset_dir)
    stats_path = f'{path_device}/Datasets/{var}/Statistics_{var}_{param}.dat'
    path_z4 = glob.glob(f'{path_device}/DATA/DD_DG_{var}_{param}/**/z4.out', recursive = True)
    path_z4 = sorted(path_z4)
    path_profile_DD = glob.glob(path_device+'/'+'DATA'+'/DD_DG_'+var+'_'+param+'/**/*-profile.dat', recursive = True)
    path_profile_MC = glob.glob(path_device+'/'+'DATA'+'/MC_SCH_'+var+'_'+param+'/**/*-profile.dat', recursive = True)
    path_profile_DD, path_profile_MC = sorted(path_profile_DD), sorted(path_profile_MC)
    df_vth = pd.read_csv(f'{path}{var}_{param}_vth.dat', sep='\t',skiprows=0)
    df_ioff = pd.read_csv(f'{path}{var}_{param}_ioff.dat',sep='\t',skiprows=0)
    df_ss = pd.read_csv(f'{path}{var}_{param}_ss.dat', sep='\t',skiprows=0)
    # Merge data in one df
    df = pd.concat([df_vth, df_ioff.drop(columns=['#Sim_id']), df_ss.drop(columns=['#Sim_id'])], axis=1)
    # Searching for z4.out in subdir, to add relevant variability columns.
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        df_ion = pd.read_csv(path+'Ion_MC_'+var+'_'+param+'.dat',sep='\t',skiprows=0)
        # Check if DD and MC profiles match
        DD_profile, MC_profile = open(path_profile_DD[0],'r'), open(path_profile_MC[0],'r')
        DD_profiletxt, MC_profiletxt = DD_profile.read(), MC_profile.read()
        if DD_profiletxt == MC_profiletxt:
            print('DD and MC profiles match')
            df = pd.concat([df,df_ion.drop(columns=['#Sim_id'],axis=1)],axis=1)
        elif DD_profiletxt != MC_profiletxt:
            print('DD and MC profiles do not match')
            df = pd.concat([df,df_ion.drop(0)],axis=0)
            # print(df_ion.drop(0))
            df['#Ion[A]'][0] = df_ion['#Ion[A]'][0]
    else:
        df = df
    for i in range(len(path_z4)):
        f = open(path_z4[i],'r')
        z4 = f.read()
        mgg_activate = re.findall(r"WF.activate[ ]*=[ ]*([\w+]*)",z4)[0]
        rd_activate = re.findall(r"RD.activate[ ]*=[ ]*([\w+]*)",z4)[0]
    # Special case for MGG variability
        if mgg_activate == 'true':
            df_wf = pd.read_csv(path+ 'mean_wf_'+param+'.dat', sep='\t',skiprows=0)
            df['#Mean WF[eV]'] = df_wf.drop(columns=['#Sim_id'])
    # Special case for RD variability
        if rd_activate == 'true':
            df_rd = pd.read_csv(path+'Number_of_dopants.dat', sep='\t',skiprows=0)
            df['#Number of dopants'] = df_rd.drop(columns=['#Sim_id'])
    cols = df.columns.tolist()
    cols = cols[1:] + cols[:1]
    df = df[cols]
    # PATH TO STORE
    df.to_csv(store_path,sep='\t',na_rep='NA',index=False)
    # Statistics of FoM
    df_clean = df.drop([0], axis=0).copy() # Removing extraction info row, and converting strings to floats, to do statistics
    # Columns to numeric format
    df_clean['#Vth[V]'], df_clean['#Ioff[A]'], df_clean['#SS[mV/dec]'] = pd.to_numeric(df_clean['#Vth[V]'],errors='coerce'),pd.to_numeric(df_clean['#Ioff[A]'],errors='coerce'), pd.to_numeric(df_clean['#SS[mV/dec]'],errors='coerce')
    # Operating with columns
    df_clean['#log10Ioff[A]'] = np.log10(df_clean['#Ioff[A]'])
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        df_clean['#Ion[A]'] = pd.to_numeric(df_clean['#Ion[A]'],errors='coerce')
        df_clean['#Ion[A/m]'] = df_clean['#Ion[A]']/Ps
    # Mean value and standar deviation of data
    f = open(stats_path, "w")
    f.write(f'''MEAN VALUES
{df_clean.mean()}

    STANDARD DEVIATION
{df_clean.std()}
''')
    f.write(f'''
Nº of subthreshold samples= {df_clean['#Vth[V]'].count()}''')
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        f.write(f'''
Nº of on samples= {df_clean['#Ion[A]'].count()}''')
    f.write(f'''
Semiconductor perimeter [m]= {Ps}''')
    f.close()
    return f
    # print(path_z4,mgg_activate)