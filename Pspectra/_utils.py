"""This is a general utilities function"""
import numpy as np
import pandas as pd
from astropy.io import fits
from scipy.signal import savgol_filter
def addRandomNoise(vector,kind='normal',noise_fraction=0.5):
    """ Add random noise

    Add pseudo random noise to the spectrum. For now only Gaussian noise is added.
    Args:
        vector (array or list) (optional): The vector that you want to make really noisy
        kind (string): The noise to be added as of now Gaussian
        noise_fraction (float) (optional): The fraction of noise to be added. 
            mean(vector)*noise_fraction will be the average value of the noise that 
            added.
    Returns:
        array: Noisy version of vector
    """
    #make vector a numpy vector
    vector = np.asarray(vector)
    #set noise level
    noise_level = np.mean(vector)*noise_fraction
    noise_vector = np.random.randn(np.size(vector))*noise_level
    #now the SNR is
    print("Mean SNR is %3.2f"%(np.mean(vector)/np.mean(noise_vector)))
    #return the noisy vector
    return (vector+noise_vector)
def readFile(filename):
    """
    Read filename

    If the file is a csv then read with pandas else with fits.
    Please provide full path.
    Args:
        filename (string): The fullpath filename of the file to be read
    Returns:
        wavelength (float array): Wavelengths
        fluxes (float array): Fluxes 
    """
    print(filename)
    filename=str(filename)
    extn=str((filename).split('/')[-1]).split('.')[-1]
    print(extn)
    if str(extn)=="csv":
        print("You are getting a Dataframe")
        data=pd.read_csv(filename, skiprows=1)    
        return (data['Wavelength (microns)'],data['Planet Flux (10^-6 erg/cm2/s/Hz)'])
    elif extn=='fits':
         #print("You are getting a fitsfile")
         data=fits.open(filename)[1].data
         return (data['Wavelength'],data['flux'])
    else:
        print("Unreadable!")
        return 0,0
    
def applyFilter(flux,window_size,order):
    """
    Apply the Savgol filter.

    Savitzky-Golay filter used in place of median filter for mean subtraction
    Args:
        flux (array): 1D spectrum vector
        window_size (int): size of window
        order (int): polynomial order of filter
    Returns:
        flux_dat (array): flux flattened
    """

    flux_filt=savgol_filter(flux,window_size,order)
    flux_dat=flux-flux_filt
    return flux_dat
def removeTelluric(wavelens,flux,wmin,wmax):
    locs_l=list(np.ravel(np.where((wavelens>=np.min(wavelens)) & (wavelens<=wmin))))
    locs_h= list(np.ravel(np.where((wavelens>=wmax) & (wavelens<=np.max(wavelens)))))
    locs=locs_l+locs_h
    flux=np.ravel(flux)
    waves=wavelens[locs]
    cut_flux=flux[locs]
    new=np.interp(wavelens,waves,cut_flux)
    return new

