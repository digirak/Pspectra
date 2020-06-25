"""This is a general utilities function"""
import numpy as np
import pandas as pd
from astropy.io import fits
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
    print("Mean SNR is %3.2f"%(np.mean(vector)/np.mean(vector)))
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

    extn=filename.split('/').split('.')[-1]
    if extn=="csv":
        #print("You are getting a Dataframe")
        data=pd.read_csv(filename)    
    elif extn=='fits':
         #print("You are getting a fitsfile")
         data=fits.open(filename)[0].data
    else:
        print("Unreadable!")
        return 0
    return (data['Wavelength (microns)'],data['Planet Flux (10^-6 erg/cm2/s/Hz)'])


