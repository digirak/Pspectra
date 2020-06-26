import numpy as np
from astropy.io import fits
from glob import glob
from scipy.interpolate import interp1d
import sys
import os
import json
from photutils import CircularAperture,aperture_photometry
import vip_hci
from scipy.signal import savgol_filter
from utils import removeTelluric, applyFilter
from astropy.convolution import Gaussian1DKernel
import warnings
from matplotlib import pyplot as plt
warnings.simplefilter('ignore', np.RankWarning)
class CrossCorr:
    def __init__(self,vels):
        self.vels=vels
        self.crosscor_dict=dict()
        self.temp_processed=0.
        self.f1=0
        self.f2=0
    def compareFluxes(self
                     ,data_wavs
                     ,data_flux
                     ,model_wavs
                     ,model_flux
                     ,window_size
                     ,order
                     ,noise=0
                     ,wmin_wmax_tellurics=[1.75,2.1]):
        vels=self.vels
        dataflux=data_flux
        final=np.zeros(len(vels))
        self.f1=dataflux-dataflux.mean()
        self.f1=removeTelluric(data_wavs,self.f1,wmin_wmax_tellurics[0],wmin_wmax_tellurics[1])

        for i in range(len(final)):
            #flux=np.convolve(flux,fwhm[0].data)
            inter=interp1d(model_wavs*(1+vels[i]/3e5),model_flux)
            temp=inter(data_wavs)
            temp_filt=applyFilter(temp
                                 ,window_size=window_size
                                 ,order=order)
            #filt=savgol_filter(temp,101,1)
            #temp_filt=temp-filt
            temp_filt=removeTelluric(data_wavs,temp_filt,wmin_wmax_tellurics[0],wmin_wmax_tellurics[1])

            self.f2=temp_filt-temp_filt.mean()
            ccov = np.correlate(self.f1,self.f2,mode='valid')
            #ccov=np.corrcoef(f1,f2)[0][1]
            cf = ccov / (self.f1.std()*self.f2.std())
            final[i]=(cf[0])
        if (noise==0):
            locs_noise_l=[(np.where(((vels>-2000)) & (vels<-1000)))]
            locs_noise_h=[(np.where(((vels>1000)) & (vels<2000)))]
            noise_floor=np.sqrt(np.std(final[locs_noise_l])**2\
            +np.std(final[locs_noise_h])**2)
        else:
            noise_floor=noise

        print("SNR is %3.2f"%(np.max(final)/noise_floor))
        return final,noise_floor,(np.max(final/noise_floor))

