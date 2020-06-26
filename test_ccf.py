import numpy as np
from CCF import  CrossCorr
from _utils import *

#read old data 
wavs,flux=readFile("/Users/rakesh/Data/Templates/BT-Settl/lte1500-3.50-0.0a+0.0.BT-settl-giant-2013.cf250.tm1.0-0.0.R1-g12p0vo1.spid.fits")
waves_downsampled=np.arange(1.4,2.4,1e-4)
flux_downsampled=np.interp(waves_downsampled,wavs,flux)
flux_noisy=addRandomNoise(flux_downsampled,noise_fraction=0.1)
vels=np.arange(-2000,2000,20)
CC=CrossCorr(vels)
window_size=101
order=1
CC.compareFluxes(waves_downsampled,
                flux_noisy,
                wavs,
                flux,
                window_size=window_size,
                order=order)
