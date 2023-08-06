# julian.garcia.fernandez2@usc.es 
# last modified: 6/Sep/2021
"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
extract_info.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This module includes the routines to create an information file with the simulation and device description, and condition used to extract the FoM to ensure reproducibility.

Example
-------
TODO
"""

import pandas as pd
import re
import sys
from datetime import date
import numpy as np 
import glob
import json
now = date.today()


def extract_info(path_subt,path_on,var,ion_input):
    """
    Methods 
    -------
    extract_info(path_subt,path_on,var,ion_input):
        Function to extract info.md with information required to describe the device, its mesh, simulation methodology and variability applied
        Output: info.md: file with information of device, dimensions, doping, variability applied and simulation methodology
        
    Parameters
    ----------
    path_subt: path
        path of subthreshold simulationss
    path_on: path
        path of on simulations
    var: string
        label of the variability applied
    param: string
        variability parameter applied to the device
    ion_input: y/n
        console asks if ion MC data is avaliable

    Return
    ------
    info.md: file
        file with information of device, dimensions, doping, variability applied and simulation methodology
	"""
    # Paths to required files to read  CHECK
    architecture, device =path_subt.split(sep='/')[-2], path_subt.split(sep='/')[-1]
    pre_geo_path = path_subt
    path_z4 = glob.glob(f'{path_subt}/**/z4.out', recursive = True)[0]
    path_z4_on = glob.glob(f'{path_on}/**/z4.out', recursive = True)
    path_sim = glob.glob(f'{path_subt}/**/*_sim.cfg', recursive = True)[0]
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        path_sim_on = glob.glob(f'{path_on}/**/*_sim.cfg', recursive = True)[0]
    print("PATH _PRE:", pre_geo_path)
    try:
        path_pre = glob.glob(f'{pre_geo_path}/*_pre.cfg', recursive = True)[0]
    except IndexError as e:
        print("_pre.cfg file not found in:", pre_geo_path)
        exit()
    try:
        path_geo = glob.glob(f'{pre_geo_path}/*.geo', recursive = True)[0]
    except IndexError as e:
        print(".geo file not found in:", pre_geo_path)
        exit()
    try:
        path_voltages = glob.glob(f'{pre_geo_path}/**/voltajes.dat', recursive = True)[0]
    except IndexError as e:
        print("voltages.dat file not found in:", pre_geo_path)
        exit()
    try:
        path_database_pre = glob.glob(f'{pre_geo_path}/database_pre.ini', recursive =True)[0]
    except IndexError as e:
        print("database_pre.ini file not found in:", pre_geo_path)
        exit()
    # Open and read sim.cfg  SUBT
    f = open(path_sim,"r")
    sim = f.read()
    WF = re.findall(r"workfunction[ ]*=[ ]*([\d+.e]*)",sim)
    mun_min = re.findall(r"mun_min[ ]*=[ ]*([\d+.e]*)",sim)
    vsat = re.findall(r"Vsat[ ]*=[ ]*([\d+.e]*)",sim)
    ECN = re.findall(r"ECN[ ]*=[ ]*([\d+.e]*)",sim)
    dg_massx = re.findall(r"massX[ ]*=[ ]*([\d+.e]*)",sim)
    dg_massy = re.findall(r"massY[ ]*=[ ]*([\d+.e]*)",sim)
    dg_massz = re.findall(r"massZ[ ]*=[ ]*([\d+.e]*)",sim)
    dg_massox = re.findall(r"massOX[ ]*=[ ]*([\d+.e]*)",sim)
    f.close()
    # Open and read sim.cfg  ON
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        f = open(path_sim_on,"r")
        sim_on = f.read()
        material_file = re.findall(r"material[ ]*=[ ]*([\d+.e]*)",sim_on)[0]
        if material_file == '0':
            material_mc_file = 'src/Include/Si_FinFET_25.dat'
        elif material_file == '1':
            material_mc_file = 'src/Include/Si_SNS3_12.dat'
        elif material_file == '2':
            material_mc_file = 'src/Include/Si_NW_5.7x7.17_Cartoixa.dat'
        elif material_file == '3':
            material_mc_file = 'src/Include/Si_NW_7.15x8.99_Cartoixa.dat'
        else:
            material_mc_file = 'Specify a material !!'
        f.close()
    # Open and read .geo CHECK
    f = open(path_geo,"r")
    geo = f.read()
    gate_length = float(re.findall(r"dXLg[ ]*=[ ]*([\d+.e]*)",geo)[0])
    source_drain_length = float(re.findall(r"dXLsd[ ]*=[ ]*([\d+.e]*)",geo)[0])
    channel_width = float(re.findall(r"Wch[ ]*=[ ]*([\d+.e]*)",geo)[0])
    channel_height = float(re.findall(r"Tch ]*=[ ]*([\d+.e]*)",geo)[0])
    w_oxide = float(re.findall(r"Wox[ ]*=[ ]*([\d+.e]*)",geo)[0])
    t_oxide = float(re.findall(r"Tox[ ]*=[ ]*([\d+.e]*)",geo)[0])
    f.close()
    # Vd from voltages.dat CHECK
    voltage = pd.read_csv(path_voltages, header=None, skiprows=1,sep='\t')
    Vd = voltage.iloc[0,-1]
    # Open and read pre.cfg CHECK
    f = open(path_pre,"r")
    pre = f.read()
    material = re.findall(r"material[ ]*=[ ]*([\w+]*)",pre) # PROBLEMAS PARA DISTINGUIR MATERIAL
    label_material = re.findall(r"\[(\w+)]*",pre)[2:]
    oxide_temp = re.findall(r"\[(oxide[\d+])]*",pre)[0]
    for idx, i in enumerate(label_material):
        if i == 'body':
            semiconductor = material[idx] 
        if i == oxide_temp:
            oxide = material[idx]
    doping_regions = re.findall(r"dopings[ ]*=[ ,]*([\w+\d+].*)",pre) 
    doping = re.findall(r"doping_type[ ]*=[ ]*([\w+]*)",pre)
    peak = re.findall(r"peak[ ]*=[ ]*([\d+.e]*)",pre)
    xchar = re.findall(r"xchar[ ]*=[ ]*([-\d+.e]*)",pre)
    xmax = re.findall(r"xmax[ ]*=[ ]*([-\d+.e]*)",pre)
    xmin = re.findall(r"xmin[ ]*=[ ]*([-\d+.e]*)",pre)
    f.close()
    # Open and read database_pre.ini  CHECK
    f = open(path_database_pre)
    database_pre = f.read()
    database_material = re.findall(r"\[(\w+)]*",database_pre)[1:]
    Nd_doping = re.findall(r"Nd[ ]*=[ ]*([\d+.e]*)",database_pre)
    Na_doping = re.findall(r"Na[ ]*=[ ]*([\d+.e]*)",database_pre)
    f.close()
    # Open and read z4.out CHECK
    f = open(path_z4,"r")
    z4 = f.read()
    title_list = []
    description_list = []
    parameter_list = []
    doi_list = []
    device_temperature = re.findall(r"Device.Temperature[ ]*=[ ]*([-\d+.e]*)",z4)[0]
    ler_activate = re.findall(r"LER.activate[ ]*=[ ]*([\w+]*)",z4)[0]
    mgg_activate = re.findall(r"WF.activate[ ]*=[ ]*([\w+]*)",z4)[0]
    ger_activate = re.findall(r"GER.activate[ ]*=[ ]*([\w+]*)",z4)[0]
    rd_activate = re.findall(r"RD.activate[ ]*=[ ]*([\w+]*)",z4)[0]
    if mgg_activate == 'true':
        title = 'MGG'
        description = 'Metal grain granularity'
        doi = '10.1109/TED.2010.2063191'
        parameter = f'''Grain size (GS)[nm]'''
        title_list.append(title),description_list.append(description),parameter_list.append(parameter),doi_list.append(doi)
    if ler_activate == 'true':
        title = 'LER'
        description = 'Line edge roughness'
        doi = '10.1016/j.sse.2016.10.018'
        parameter = f'''Correlation length (CL)[nm]; Root mean square(RMS)[nm]'''
        title_list.append(title),description_list.append(description),parameter_list.append(parameter),doi_list.append(doi)
    if ger_activate == 'true':
        title = 'GER'
        description = 'Gate edge roughness'
        doi = '10.1109/LED.2019.2900494'
        parameter = f'''Correlation length (CL)[nm]; Root mean square(RMS)[nm]'''
        title_list.append(title),description_list.append(description),parameter_list.append(parameter),doi_list.append(doi)
    if rd_activate == 'true':
        title = 'RD'
        description = 'Random dopants'
        doi = '10.1109/TED.2009.2027973'
        parameter = f'''Number of dopants[#]'''
        title_list.append(title),description_list.append(description),parameter_list.append(parameter),doi_list.append(doi)
    f.close()
    # Writing info.md & info.json
    dateStr = now.strftime("%d %b %Y")
    path_save_json = pre_geo_path+'/Datasets/'+title+'/info.json'
    path_save_md = pre_geo_path+'/Datasets/'+title+'/info.md'
    info_dict = {}
    info_dict['title'] = 'info.json'
    info_dict['date'] = dateStr
    info_dict['contact_point'] = 'julian.garcia.fernandez2@usc.es'
    save_info = open(path_save_md,'w')
    save_info.write(f'''# Title: info.md
### **Description:** 
This file contains the information needed to understand data results. It includes information about the architecture, dimensions, materials, variability applied, simulation methodology, doping characteristics and data content.
##### **Update:** {now}
##### **Contact point:** julian.garcia.fernandez2@usc.es
''')
    save_info.write(f'''### **Architecture: {architecture}**
''')
    info_dict['architecture'] = architecture
    save_info.write(f'''**Dimensions:**
* Gate length [nm]: {gate_length}
* Source/Drain length [nm]: {source_drain_length/2}
* Channel height [nm]: {channel_height}
* Channel width [nm]: {channel_width}
* Oxide width [nm]: {w_oxide}
* Oxide height [nm]: {t_oxide}
''')
    info_dict['dimensions'] = {
    'gate_length':gate_length,
    'source_drain_length': source_drain_length,
    'channel_height': channel_height,
    'channel_width': channel_width,
    'oxide_width': w_oxide,
    'oxide_height': t_oxide}
    if architecture == 'FinFET':
        top_buried = input('Top oxide height [nm] = ')
        save_info.write(f'''* Top oxide height [nm]: {top_buried}
''')
        info_dict['dimensions'] = {'gate_length':gate_length,
    'source_drain_length': source_drain_length,
    'channel_height': channel_height,
    'channel_width': channel_width,
    'oxide_width': w_oxide,
    'oxide_height': t_oxide,
    'top_oxide_height': top_buried}
    for idx, i in enumerate(database_material):
        if i == semiconductor:
            save_info.write(f'''
**Semiconductor:**
* Material: **{semiconductor}**
* Nd [cm^-3]: {Nd_doping[idx]}
* Na [cm^-3]: {Na_doping[idx]}
''')       
            info_dict['semiconductor'] = {
            'material': semiconductor,
            'nd': Nd_doping[idx],
            'na': Na_doping[idx],
            }
        if i == oxide:
            save_info.write(f'''
**Oxide:**
* Material: **{oxide}**
''')
            info_dict['oxide'] = {'material': oxide}
            if float(Na_doping[idx]) or float(Nd_doping[idx]) != 0.0:
                print(f'''* Nd [cm^-3]: {Nd_doping[idx]}
* Na [cm^-3]: {Na_doping[idx]}
''')
    save_info.write(f'''
**Workfunction [eV]:** {WF[0]}

**Drain voltage [V]:** {Vd}

**Device temperature [K]:** {device_temperature}
''')
    info_dict['workfunction'] = WF[0]
    info_dict['drain_voltage'] = Vd
    info_dict['device_temperature'] = device_temperature
    save_info.write(f'''
**Gaussian doping profile(s):**
* doping_regions = {doping_regions}
* doping_type = {doping}
* peak [cm^-3] = {[float(i) for i in peak]} 
* xchar [nm]= {[round(float(i)*1000,3) for i in xchar]} 
* xmax [nm]= {[round(float(i)*1000,3) for i in xmax]} 
* xmin [nm]= {[round(float(i)*1000,3) for i in xmin]} 
''')
    info_dict['gaussian_doping_profiles'] = {'doping_regions': doping_regions,
    'doping_type': doping,'peak': [float(i) for i in peak], 'xchar': [round(float(i)*1000,3) for i in xchar],
    'xmax': [round(float(i)*1000,3) for i in xmax], 'xmin': [round(float(i)*1000,3) for i in xmin]}
    # Simulation methodology
    f = open(path_z4,"r")
    z4 = f.read()
    MC_activate = re.findall(r"MC.activate[ ]*=[ ]*([\w+]*)",z4)[0]
    sch_orientation = re.findall(r"SCH.orientation[ ]*=[ ]*([\d+.e]*)",z4)[0]
    sch_activate, dg_activate = re.findall(r"SCH.activate[ ]*=[ ]*([\w+]*)",z4)[0], re.findall(r"DG.activate[ ]*=[ ]*([\w+]*)",z4)[0]
    if MC_activate == 'true':
        sim_subt_method = '3D Monte Carlo' 
    else:
        sim_subt_method = 'Drift diffusion transport method'
    save_info.write(f'''
**Subthreshold region simulation methodology:** 
* **{sim_subt_method}**
''')
    info_dict['subthreshold_region_simulation_methodology'] = sim_subt_method
    if sch_activate == 'true':
        QC = '2D Shrödinger equation'
        save_info.write(f'''* Quantum corrections: **{QC}**
* SCH slices orientation: {sch_orientation}''')
        info_dict['subthreshold_region_simulation_methodology'] = {'simulation_methodolgy': sim_subt_method,
        'quantum_corrections': {'quantum_correction_type': QC,'sch_orientation': sch_orientation}}
    elif dg_activate == 'true':
        QC = 'Density gradient'
        save_info.write(f'''* Quantum corrections: **{QC}**
* Density gradient masses:
    * MassX: {dg_massx[0]}
    * MassY: {dg_massy[0]}
    * MassZ: {dg_massz[0]}
    * MassOX: {dg_massox[0]}
''')
        info_dict['subthreshold_region_simulation_methodology'] = {'simulation_methodolgy': sim_subt_method,
        'quantum_corrections': {'quantum_correction_type': QC,
        'density_gradient_masses': {'massX': dg_massx[0],'massY': dg_massy[0],'massZ': dg_massz[0],'massOX':dg_massox[0]}}}
    else:
        QC = 'No quantum correction applied'
        save_info.write(f'''* Quantum corrections: {QC}''')
    f.close()
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        f = open(path_z4_on[0],"r")
        z4_on = f.read()
        MC_activate_on = re.findall(r"MC.activate[ ]*=[ ]*([\w+]*)",z4_on)[0]
        MC_particulas_totales = re.findall(r"MC_.PARTICULAS_TOTALES[ ]*=[ ]*([\d+.e]*)",z4_on)[0]
        MC_particulas_contactos_ini = re.findall(r"MC_.PART_CONTACTOS_INI[ ]*=[ ]*([\d+.e]*)",z4_on)[0]
        MC_time_sim = re.findall(r"MC_.TIME_SIMUL[ ]*=[ ]*([\d+.e-]*)",z4_on)[0]
        MC_sr_cl =re.findall(r"MC_.sr_cl[ ]*=[ ]*([\d+.e-]*)",z4_on)[0]
        MC_sr_rms =re.findall(r"MC_.sr_rms[ ]*=[ ]*([\d+.e-]*)",z4_on)[0]
        sch_orientation_on = re.findall(r"SCH.orientation[ ]*=[ ]*([\d+.e]*)",z4_on)[0]
        sch_activate_on, dg_activate_on = re.findall(r"SCH.activate[ ]*=[ ]*([\w+]*)",z4_on)[0], re.findall(r"DG.activate[ ]*=[ ]*([\w+]*)",z4_on)[0]
        if MC_activate_on == 'true' or MC_activate_on == 'True':
            sim_on_method = '3D Monte Carlo'
        else:
            sim_on_method = 'Drift diffusion transport method'
        save_info.write(f'''
**On region simulation methodology:** 
* **{sim_on_method}**
* Monte Carlo simulation parameters:
    * Total particles [#]: {MC_particulas_totales}
    * Initial contact particles [#]: {MC_particulas_contactos_ini}
    * MC simulation time [s]: {MC_time_sim}
    * Surface roughness scattering using autocorrelation function ACF:
        * RMS height [nm]: {MC_sr_rms}
        * Correlation length [nm]: {MC_sr_cl}
    * Material file: {material_mc_file}
''')
        if sch_activate_on == 'true':
            QC_on = '2D Shrödinger equation'
            save_info.write(f'''* Quantum corrections: **{QC_on}**
    * SCH slices orientation: {sch_orientation_on}
''')
            info_dict['on_region_simulation_methodology'] = {'simulation_methodolgy': sim_on_method,
            'MC_sim_parameters': {'total_particles': MC_particulas_totales,'MC_cont_particles_ini': MC_particulas_contactos_ini,
            'MC_sim_time': MC_time_sim,'sr_parameters': {'sr_rms': MC_sr_rms,'sr_cl': MC_sr_cl},'material_file': material_mc_file},
            'quantum_corrections': {'quantum_correction_type': QC_on,'sch_orientation': sch_orientation_on}}
        elif dg_activate_on == 'true':
            QC_on = 'Density gradient'
            info_dict['on_region_simulation_methodology'] = {'simulation_methodolgy': sim_on_method,
            'MC_sim_parameters': {'total_particles': MC_particulas_totales,'MC_cont_particles_ini': MC_particulas_contactos_ini,
            'MC_sim_time': MC_time_sim,'sr_parameters': {'sr_rms': MC_sr_rms,'sr_cl': MC_sr_cl},'material_file': material_mc_file},
            'quantum_corrections': {'quantum_correction_type': QC_on,
            'density_gradient_masses': {'massX': dg_massx[0],'massY': dg_massy[0],'massZ': dg_massz[0],'massOX':dg_massox[0]}}}
            save_info.write(f'''
* Quantum corrections: {QC_on}
* Density gradient masses:
    * MassX: {dg_massx[0]}
    * MassY: {dg_massy[0]}
    * MassZ: {dg_massz[0]}
    * MassOX: {dg_massox[0]}
''')
        else:
            QC_on = 'No quantum correction applied'
            info_dict['on_region_simulation_methodology'] = {'simulation_methodolgy': sim_on_method,
            'MC_sim_parameters': {'total_particles': MC_particulas_totales,'MC_cont_particles_ini': MC_particulas_contactos_ini,
            'MC_sim_time': MC_time_sim,'sr_parameters': {'sr_rms': MC_sr_rms,'sr_cl': MC_sr_cl},'material_file': material_mc_file},
            'quantum_correction_type': QC_on}
            save_info.write(f'''
* Quantum corrections: {QC_on}
''')
        f.close()
    else:
        print('No On region data')
    save_info.write(f'''
**Simulation info:**
* Minimun Mobility [cm²/Vs]: {mun_min[0]} 
* Critical Electric Field [V/cm]: {ECN[0]}
* Saturation velocity [cm²/s]: {vsat[0]}
''')
    info_dict['simulation_info'] = {'minimun_mobility': mun_min[0],'critical_electric_field': ECN[0],'saturation_velocity': vsat[0]} 
    # FoM EXTRACTION INFO
    path_dataframe = glob.glob(f'{pre_geo_path}/Datasets/{var}/DF_*',recursive = True)[0]
    f = open(path_dataframe,"r")
    df = f.read()
    ioff_criteria = re.findall(r"(Vg=[\d+.e]*)",df)[0]
    ss_criteria = re.findall(r"Vg_int=([\d+.e]*[, ]*[\d+.e]*)",df)[0]
    vth_criteria = re.findall(r"([\w+]*)[ ]*method",df)[0]
    ion_criteria = re.findall(r"Vg_on=([\d+.e]*)",df)
    if vth_criteria == 'CC':
        criteria = 'Constant current criteria [A]'
        current_cc = re.findall(r"(Icc=[\d+.e+-]*)",df)[0]
    elif vth_criteria == 'LE':
        current_cc = ''
        criteria = 'Linear extrapolation'
    elif vth_criteria == 'SD':
        current_cc = ''
        criteria = 'Second derivative'
    elif vth_criteria == 'TD':
        current_cc = ''
        criteria = 'Third derivative'
    f.close()
    # DATA CONTENT
    if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
        info_dict['data_content'] = {'id': '#Sim_id','threshold_voltage':{'label': '#Vth[V]','extraction_method': criteria,'current_cc': current_cc},
        'off_current':{'label': '#Ioff[A]','gate_voltage': ioff_criteria}, 'subthreshold_slope': {'label': '#SS[mV/dec]','gate_voltage_interval': ss_criteria},
        'on_current':{'label': '#Ion[A]','gate_voltage': ion_criteria}}
        save_info.write(f'''
**Data content:**
* Identification for each simulation: #Sim_id
* Threshold voltage: #Vth[V]
    * Extraction method used: {criteria}, {current_cc}
* Off current: #Ioff[A]
    * Extraction method used: Gate voltage [V], {ioff_criteria}
* Subthreshold slope: #SS[mV/dec]
    * Extraction method used: Gate voltage interval [V], ({ss_criteria})
* On current: #Ion[A]
    * Extraction method used: Gate voltage [V], {ion_criteria}
''') 
    else: 
        info_dict['data_content'] = {'id': '#Sim_id','threshold_voltage':{'label': '#Vth[V]','extraction_method': criteria,'current_cc': current_cc},
    'off_current':{'label': '#Ioff[A]','gate_voltage': ioff_criteria}, 'subthreshold_slope': {'label': '#SS[mV/dec]','gate_voltage_interval': ss_criteria}}
        save_info.write(f'''
**Data content:**
* Identification for each simulation: #Sim_id
* Threshold voltage: #Vth[V]
    * Extraction method used: {criteria}, {current_cc}
* Off current: #Ioff[A]
    * Extraction method used: Gate voltage [V], {ioff_criteria}
* Subthreshold slope: #SS[mV/dec]
    * Extraction method used: Gate voltage interval [V], ({ss_criteria})
''')
    if mgg_activate == 'true':
        save_info.write(f'''* Mean work function of the gate: #Mean WF[eV]
''')
    if rd_activate == 'true':
        save_info.write(f'''* Number of dopants: #Number of dopants
''')
        if ion_input == 'yes' or ion_input == 'y' or ion_input == 'true':
            info_dict['data_content'] = {'id': '#Sim_id','threshold_voltage':{'label': '#Vth[V]','extraction_method': criteria,'current_cc': current_cc},
            'off_current':{'label': '#Ioff[A]','gate_voltage': ioff_criteria}, 'subthreshold_slope': {'label': '#SS[mV/dec]','gate_voltage_interval': ss_criteria},
            'on_current':{'label': '#Ion[A]','gate_voltage': ion_criteria},'number_of_dopants':'#Number of dopants'}
        else:
            info_dict['data_content'] = {'id': '#Sim_id','threshold_voltage':{'label': '#Vth[V]','extraction_method': criteria,'current_cc': current_cc},
            'off_current':{'label': '#Ioff[A]','gate_voltage': ioff_criteria}, 'subthreshold_slope': {'label': '#SS[mV/dec]','gate_voltage_interval': ss_criteria},
            'on_current':{'label': '#Ion[A]'},'number_of_dopants':'#Number of dopants'}
    # VARIABILITY
    info_dict['variability_source'] = {'variability': title_list,'decription': description_list,'doi': doi_list,'parameter(s)': parameter_list}
    save_info.write(f'''
**Variability source: {title_list}**
* Description: {description_list}
* doi: {doi_list}
* Parameter(s): {parameter_list}
''')
    # VENDES VERSION
    info_dict['vendes_version'] = 'TODO'
    save_info.write(f'''
**VENDES version**: TODO
''')
    # COMPILADOR VERSION
    info_dict['comp_libraries_version'] = 'TODO'
    save_info.write(f'''
**Compiler and libraries version**: TODO
''')
    save_info.close()
    save_info_json = open(path_save_json,'w')
    json.dump(info_dict,save_info_json)
    return save_info, save_info_json