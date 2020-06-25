"""This adds random noise to the function"""
import numpy as np
def addRandomNoise(vector,kind='normal',noise_fraction=0.5):
    """ Add random noise

    Add pseudo random noise to the spectrum. For now only Gaussian noise is added.
    Args:
        vector (array or list) (optional): The vector that you want to make really noisy
        kind (string): The noise to be added as of now Gaussian
        noise_fraction (float) (optional): The fraction of noise to be added. 
            Max(vector)*noise_fraction will be the average value of the noise that 
            added.
    Returns:
        array: Noisy version of vector
    """
    vector=np.asarray(vector)

