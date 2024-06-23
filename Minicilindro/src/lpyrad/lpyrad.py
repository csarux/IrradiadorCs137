'''
File: lpyrad.py
Cësar Rodríguez
Description: Axuiliary funntions to analyze the dosse distributions measured at UCM Cs-137 irradiator
Version: 0.1.0
'''
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt

def read_dose(dxf):
    '''
    Function: read_dose
    Read a dxf file into a pandas dataframe

    Arguments:
    dxf: String
    dxf filename

    Returns:
    dosedf: pandas dataframe
    Dose distribution. 
    The column names are the pixel y positions in cm.
    The index are the pixel x positions in cm.
    '''    
    Size1Header = 7
    GeneralHeader = 48
    tdf = pd.read_csv(dxf, sep='=', skiprows=Size1Header, nrows=2)
    cols = int( tdf.iloc[0].X)
    pxsz = tdf.iloc[1].X/10
    dosedf = pd.read_csv(dxf, sep='\t', skiprows=GeneralHeader, names=np.linspace(1,cols*pxsz+1, cols))
    return dosedf


def dose_plane_plot(dose_dict, plane, minimum, maximum, step, ax, cmap=plt.cm.gray_r, alpha=0.5, fontsize=10):
    '''
    Function: dose_plane_plot
    Function to plot a measured dose plane distribution
    
    Arguments:
    dose_dict: dictionary
    Pandas dataframe dictionary of dose distributions
    plane: string
    The dose plane name
    minimum: float
    The minumum dose level to plot
    maximum: float
    The maximum dose level to plot
    step: float
    The dose difference between isodose levels
    ax: axis
    The axis to plot in
    cmap: matplotlib colormap
    Plot colormap 
    alpha: matplotlib alpha
    The color transparancy to fill the isodose levels
    fontsize: integer
    The isodose label fontsize
    
    Returns: None
    '''
    numy, numx = dose_dict[plane].values.shape
    pxsz = dose_dict['V.1.c999.dxf'].columns[1] - dose_dict['V.1.c999.dxf'].columns[0]
    x = np.linspace(numx*pxsz, 0, numx)
    y = np.linspace(0, numy*pxsz, numy)
    X, Y = np.meshgrid(x, y)
    ax.contourf(X, Y, dose_dict[plane].values, cmap=cmap, levels=np.arange(minimum, maximum, step), alpha=alpha)
    cont = ax.contour(X, Y, dose_dict[plane].values, cmap=cmap, levels=np.arange(minimum, maximum, step))
    ax.clabel(cont, inline=1, fontsize=fontsize)
    ax.set_xlabel('Y [cm]')
    ax.set_ylabel('X [cm]')
    return

def mean_dose_plane_plot(dose_plane, minimum, maximum, step, ax, dpi=72, cmap=plt.cm.gray_r, alpha=0.5, fontsize=10):
    '''
    Function: mean_dose_plane_plot
    Function to plot a measured dose plane distribution
    
    Arguments:
    dose_plane: numpy array
    numpy aray of the dose distributions
    minimum: float
    The minumum dose level to plot
    maximum: float
    The maximum dose level to plot
    step: float
    The dose difference between isodose levels
    ax: axis
    The axis to plot in
    dpi: integer
    scanned image dot per inche 
    cmap: matplotlib colormap
    Plot colormap 
    alpha: matplotlib alpha
    The color transparancy to fill the isodose levels
    fontsize: integer
    The isodose label fontsize
    
    Returns: None
    '''
    numy, numx = dose_plane.shape
    pxsz = 2.54/dpi
    x = np.linspace(numx*pxsz, 0, numx)
    y = np.linspace(0, numy*pxsz, numy)
    X, Y = np.meshgrid(x, y)
    ax.contourf(X, Y, dose_plane, cmap=cmap, levels=np.arange(minimum, maximum, step), alpha=alpha)
    cont = ax.contour(X, Y, dose_plane, cmap=cmap, levels=np.arange(minimum, maximum, step))
    ax.clabel(cont, inline=1, fontsize=fontsize)
    ax.set_xlabel('Y [cm]')
    ax.set_ylabel('X [cm]')
    return

def to_shape(a=None, shape=None, mode='empty'):
    '''
    Function: to_shape
    Shape an array to other shape
    
    Arguments:
    a: numpy array
    The array to shape
    shape: sequence like
    The targetshape
    mode: string
    The mode as in np.pad funtion
    
    Returns:
    ashaped: numpy array
    The shaped array
    '''
    y_, x_ = shape
    y, x = a.shape
    y_pad = (y_-y)
    x_pad = (x_-x)
    ashaped = np.pad(a,((y_pad//2, y_pad//2 + y_pad%2), 
                     (x_pad//2, x_pad//2 + x_pad%2)),
                  mode = 'constant')
    return ashaped

def mds_dose_plane_plot(minimum, maximum, step, ax, cdose=25, cmap=plt.cm.gray_r, alpha=0.5, fontsize=10):
    '''
    Function: mds_dose_plane_plot
    Function to plot the documented dose plane distribution
    
    Arguments:
    minimum: float
    The minumum dose level to plot
    maximum: float
    The maximum dose level to plot
    step: float
    The dose difference between isodose levels
    ax: axis
    The axis to plot in
    cdose: float
    central dose value
    cmap: matplotlib colormap
    Plot colormap 
    alpha: matplotlib alpha
    The color transparancy to fill the isodose levels
    fontsize: integer
    The isodose label fontsize
    
    Returns: None
    '''
    dose_plane = np.array(
        [
            [24.7, 23.2, 22.4, 22.3, 22.4, 23.2, 24.3],
            [24.9, 23.6, 22.6, 22.4, 22.6, 23.6, 24.7],
            [25.4, 24.0, 23.3, 23.2, 23.5, 24.3, 25.2],
            [26.2, 24.8, 23.9, 23.8, 24.1, 24.8, 25.7],
            [26.9, 24.9, 24.2, 24.1, 24.6, 25.4, 26.5],
            [27.4, 25.6, 24.6, 24.4, 24.7, 25.6, 26.8],
            [27.7, 25.8, 24.9, 24.7, 25.0, 26.0, 27.1],
            [28.0, 26.1, 25.2, 24.9, 25.2, 26.2, 27.4],
            [27.7, 26.1, 25.1, 25.0, 25.3, 26.2, 27.5],
            [27.8, 25.8, 24.9, 24.7, 25.2, 26.1, 27.2],
            [27.8, 25.9, 25.3, 24.7, 25.2, 26.1, 27.3],
            [27.1, 25.6, 24.7, 24.7, 24.8, 25.8, 26.9],
            [26.9, 25.2, 24.3, 24.3, 24.5, 25.3, 26.9],
            [26.6, 25.0, 24.1, 23.7, 24.2, 25.0, 26.6],
            [26.0, 24.6, 23.2, 23.0, 23.3, 24.5, 26.0],
            [25.4, 23.5, 22.7, 22.5, 23.0, 24.0, 25.3],
            [23.9, 22.3, 21.4, 21.3, 21.6, 22.4, 24.0],
        ]
    )
    dose_plane = dose_plane.transpose() / 25 * cdose
    numy, numx = dose_plane.shape
    x = np.linspace(0., 16.4, numx)
    y = np.linspace(0., 6., numy)
    X, Y = np.meshgrid(x, y)
    ax.contourf(X, Y, dose_plane, cmap=cmap, levels=np.arange(minimum, maximum, step), alpha=alpha)
    cont = ax.contour(X, Y, dose_plane, cmap=cmap, levels=np.arange(minimum, maximum, step))
    ax.clabel(cont, inline=1, fontsize=fontsize)
    ax.set_xlabel('Y [cm]')
    ax.set_ylabel('X [cm]')
    return
