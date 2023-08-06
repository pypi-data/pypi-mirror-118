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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, norm
import os

def scatter_plot_subt(df_path,var,param,save_plot,x_lim=None,y_iofflim=None,y_sslim=None):
    """
    Methods 
    -------
    scatter_plot_subt(df_path,var,param,save_plot,x_lim=None,y_iofflim=None,y_sslim=None):
        function to generate logIoff vs Vth and Vth vs SS scatter subplots in one figure
        
    Parameters
    ----------
    df_path: path
        path of dataframe
    save_plot: path
        path of the device simulations
    var: string
        label of the variability applied
    param: string
        variability parameter applied to the device
    x_lim: float interval
        x-axis interval
    y_ioffliml: float interval
        y-axis limit on logIoff subplot
    y_sslim: float interval
        y-axis limit on SS subplot

    Return
    ------
    var_param_scatter_plot.png: PNG file
        figure with the two scatter plots.
	"""
    device = df_path.split(sep='/')[1]
    df = pd.read_csv(df_path,sep='\t')
    df_clean = df.drop([0], axis=0) # Removing extraction info row, and converting strings to floats, to do statistics
    fig_size = (12,7)
    fig, axes = plt.subplots(1,2,figsize=fig_size)
    df_clean['#Vth[V]'], df_clean['#Ioff[A]'], df_clean['#SS[mV/dec]'] = pd.to_numeric(df_clean['#Vth[V]'],errors='coerce'),pd.to_numeric(df_clean['#Ioff[A]'],errors='coerce'), pd.to_numeric(df_clean['#SS[mV/dec]'],errors='coerce')
    df_clean['#log10Ioff[A]'] = np.log10(df_clean['#Ioff[A]'])
    df_subt = df_clean.dropna(subset=["#Vth[V]",'#log10Ioff[A]']) #droping subt NaNs
    rho_vi = pearsonr(df_subt["#Vth[V]"],df_subt["#log10Ioff[A]"])
    rho_vss = pearsonr(df_subt["#Vth[V]"],df_subt["#SS[mV/dec]"])
    label_vioff = f'{var}:{param}\nCorrelation={rho_vi[0]:.3f}'
    label_vss = f'{var}:{param}\nCorrelation={rho_vss[0]:.3f}'
    df_clean.plot(x="#Vth[V]",y="#log10Ioff[A]",kind='scatter',s=50,color='m',marker='x',label=label_vioff,xlim=x_lim,ylim=y_iofflim,fontsize=15, ax=axes[0])
    axes[0].set_xlabel('Vth [V]', size = 20)
    axes[0].set_ylabel('log(Ioff) [A]',size = 20)
    axes[0].legend(prop={'size':20})
    df_clean.plot(x="#Vth[V]",y="#SS[mV/dec]",kind='scatter',s=50,color='b',marker='x',label=label_vss,xlim=x_lim,ylim=y_sslim,fontsize=15, ax=axes[1])
    axes[1].set_xlabel('Vth [V]', size = 20)
    axes[1].set_ylabel("SS [mV/dec]",size = 20)
    axes[1].legend(prop={'size':20})
    plt.suptitle(t=f'''{device} {var}''',fontsize=20)
    if not os.path.exists(save_plot):
        os.makedirs(save_plot)
        print("Scatter plot directory created:", save_plot)
    return plt.savefig(f'{save_plot}/{var}_{param}_scatter.png')

def ss_hist(df_path,var,param,save_plot):
    """
    Methods 
    -------
    ss_hist(df_path,var,param,save_plot):
        histogram of the subthreshold slope

    Parameters
    ----------
    df_path: path
        path of dataframe
    save_plot: path
        path of the device simulations
    var: string
        label of the variability applied
    param: string
        variability parameter applied to the device

    Return
    ------
    ss_hist_var_param.png: PNG file
        figure with the SS histogram.
	"""
    device = df_path.split(sep='/')[1]
    df = pd.read_csv(df_path,sep='\t')
    df_clean = df.drop([0], axis=0)
    df_clean['#SS[mV/dec]'] = pd.to_numeric(df_clean['#SS[mV/dec]'],errors='coerce')
    df_clean.plot.hist(by='#SS[mV/dev]',bins=20,alpha=0.5,edgecolor = 'black')
    plt.axvline(df_clean['#SS[mV/dec]'].mean(), color='r', linestyle='dashed', linewidth=2)
    plt.title(f'''$\mu$={df_clean['#SS[mV/dec]'].mean():.2f}, $\sigma$={df_clean['#SS[mV/dec]'].std():.2f}''')
    if not os.path.exists(save_plot):
        os.makedirs(save_plot)
        print("Scatter plot directory created:", save_plot)
    return plt.savefig(f'{save_plot}/ss_hist_{var}_{param}.png')

def ioff_hist(df_path,var,param,save_plot):
    """
    Methods 
    -------
    ioff_hist(df_path,var,param,save_plot):
        histogram of the subthreshold slope

    Parameters
    ----------
    df_path: path
        path of dataframe
    save_plot: path
        path of the device simulations
    var: string
        label of the variability applied
    param: string
        variability parameter applied to the device

    Return
    ------
    ioff_hist_var_param.png: PNG file
        figure with the Ioff histogram.
	"""
    device = df_path.split(sep='/')[1]
    df = pd.read_csv(df_path,sep='\t')
    df_clean = df.drop([0], axis=0)
    df_clean['#Ioff[A]'] = pd.to_numeric(df_clean['#Ioff[A]'],errors='coerce')
    # df_clean['#log10Ioff[A]'] = np.log10(df_clean['#Ioff[A]'])
    df_clean.plot.hist(by='#Ioff[A]',bins=50,alpha=0.5,edgecolor = 'black',color='r')
    plt.axvline(df_clean['#Ioff[A]'].mean(), color='b', linestyle='dashed', linewidth=2)
    plt.title(f'''$\mu$={df_clean['#Ioff[A]'].mean():.2e}, $\sigma(logioff)$={np.log10(df_clean['#Ioff[A]']).std():.2f}''')
    if not os.path.exists(save_plot):
        os.makedirs(save_plot)
        print("Scatter plot directory created:", save_plot)
    return plt.savefig(f'{save_plot}/ioff_hist_{var}_{param}.png')