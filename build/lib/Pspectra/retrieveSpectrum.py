from __future__ import print_function, division
import numpy as np
import pylab as plt
import os
import random
from itertools import cycle, chain
import json
from scipy.interpolate import interp1d
import csv

from petitRADTRANS import Radtrans
from petitRADTRANS import nat_cst as nc
from .calc_MMW import calc_MMW

from Pspectra.Data import Data 
from Pspectra.calcSpectrum import Spectrum

class retrieveSpec: 
    
    def __init__(self, data_folder, data_filename, N_temp, state_T, elements, N_ab, state_ab,\
                 spectrum_folder, delta, wlmin, wlmax, mode, scatt): 
        
        self.data_folder=  data_folder
        self.data_filename = data_filename
        
        self.data= Data(self.data_folder, self.data_filename)
        self.parameters= self.data.json_to_dict()                 #('Data/Molliere_without_clouds.json')
        
        try: 
            self.pmin= self.parameters['pmin']
            self.pmax= self.parameters['pmax']
            self.R= self.parameters['R']
            self.gravity= self.parameters['g']
            self.kappa_IR= self.parameters['kappa_IR']
            self.gamma= self.parameters['gamma']
            self.T_int= self.parameters['T_int']
            self.T_equ= self.parameters['T_equ']
            
        except: 
            pass
        
        self.N_temp= N_temp
        self.state_T= state_T
        self.elements= elements
        self.N_ab= N_ab
        self.state_ab= state_ab
        self.spectrum_folder= spectrum_folder + '_'.join(list(self.parameters['ab'].keys()))
        self.delta= delta
        self.wlmin= wlmin
        self.wlmax= wlmax
        self.mode = mode
        self.scatt= scatt
        
        self.spectrum=Spectrum(self.N_temp, self.state_T, self.elements,self.N_ab, self.state_ab,\
                               self.spectrum_folder, self.delta, self.wlmin, self.wlmax)
        

    def obtaining_data(self):

        #MMW= self.parameters['MMW']
        ab= self.parameters['ab']
        MMW = calc_MMW(ab)
        gravity = self.parameters['g']
        
        if self.data.check_valueORfile(ab):            #checking whether file 
            pressures = np.array(self.parameters['P'])
            temperature = self.parameters['T']
            abundances = {}
            for el in ab: 
                abundances[el] = np.array(ab[el])
                
            
            
        else:                                     #checking whether value
            pressures = self.spectrum.Pressure(self.pmin, self.pmax, self.R)    
            MMW = MMW * np.ones_like(pressures)
            temperature= self.spectrum.guillot(self.kappa_IR, self.gamma, gravity, self.T_int, self.T_equ, pressures)
            abundances = {}
            for el in ab: 
                abundances[el] = ab[el]* np.ones_like(pressures)
        

        return  pressures, temperature, abundances, gravity, MMW 
    
    def __call__(self): 
        
        pressures, temperature, abundances, gravity, MMW = self.obtaining_data()
        abK= list(abundances.keys())

        Spect = {}
        for j in np.arange(self.N_temp):         #### Temperature variations #### 
            
            temperature, percent = self.spectrum.varyingT(temperature, j) 
            #print(temperature)
            for i in np.arange(self.N_ab):      #### Abundance variations #### 
                    

                    a,b,p_a,p_b,p_e= self.spectrum.varyingAbundance(abundances, i) ##finding abundances #####                          
                    #print(a,b)
                    wl, fl= self.spectrum.calculating_spectrum(a, b, pressures, temperature, gravity, MMW, self.mode, self.scatt)  ##calculating spectrum ######

                    #saving and returning the spectrum 
                    
                    Spect = self.spectrum.saving_spectrum(Spect, wl,fl, temperature, percent, a.keys(), p_a, b.keys(), p_b, i+j)
                    
                    #print(j,i, 'percent ', percent)
                    
                    #plotting and saving the plot 
                    self.spectrum.plotting_PTprofile(pressures, temperature, percent)
                    self.spectrum.plotting_spectrum(wl,fl,percent,i, p_a,p_b, p_e, abK)
                    
        return Spect           