from __future__ import print_function, division

import numpy as np
from petitRADTRANS import Radtrans
from petitRADTRANS import nat_cst as nc
import pylab as plt
import os
import random
from itertools import cycle, chain
import json
from scipy.interpolate import interp1d
import csv

class Spectrum: 
    
    def __init__(self, N_temp, state_T, elements, N_ab, state_ab, spectrum_folder, delta, wlmin, wlmax):
        
        self.N_temp= N_temp
        self.state_T= state_T
        self.elements= elements
        self.N_ab= N_ab
        self.state_ab= state_ab
        self.spectrum_folder= spectrum_folder 
        self.delta= delta
        self.wlmin= wlmin
        self.wlmax= wlmax
        
        if not os.path.exists(self.spectrum_folder): 
            os.system('mkdir '+ self.spectrum_folder)               ###### making the spectrum folder #######

    def Pressure(self, pmin, pmax, R): 
        pressures = np.logspace(pmin, pmax, R)
        return pressures   
    
    def guillot(self, kappa_IR, gamma, gravity, T_int, T_equ, pressures): 
        temperature = nc.guillot_global(pressures, kappa_IR, gamma, gravity, T_int, T_equ)
        return temperature 

    def Toggle(self, v, i):    # v is an array ; will Toggle an array about delta %
        if i==0:
            return v- np.multiply(v, (self.delta/100))     # -20 %
        else : 
            return v+ np.multiply(v, (self.delta/100))     # +20 %
                     
    def Random(self, v, N=20):    
        p = np.round(np.random.uniform(-self.delta, self.delta, 1)) # to randomly pick a value between the range np.linspace(-self.delta, self.delta, N)
        v = v+ np.multiply(v, (p /100)) 
        return v , p                   
        
        
    def varyingT(self, temperature, i): 
        
        percent=0
        
        if self.state_T=='toggle': 
            temperature = self.Toggle(temperature,i)
            if i==0:
                percent = -self.delta
            else:
                percent = self.delta
    
        if self.state_T=='random': 
            temperature, percent = self.Random(temperature, self.N_temp) 
        return temperature , percent

    def varyingAbundance(self, ab, i): #state= toggle/random 
        a={} 
        b={}
        p_a={}
        p_b={}
        p_e={}
    
        for e in self.elements:                   # elements to be varied
            if self.state_ab == None : 
                if (e=='H2') | (e=='He'):      
                    b[e] = ab[e]
                else:
                    a[e] = ab[e]
            if self.state_ab =='toggle': 
                if (e=='H2') | (e=='He'): 
                    b[e] = self.Toggle(ab[e],i)
                    if i==0:
                        p_b[e] = -self.delta
                    else: 
                        p_b[e] = self.delta
                else: 
                    a[e] = self.Toggle(ab[e],i)
                    if i==0:
                        p_a[e] = -self.delta
                    else: 
                        p_a[e] = self.delta
                                               
                
            if self.state_ab =='random': 
                if (e=='H2') | (e=='He'): 
                    b[e], p_b[e] = self.Random(ab[e], self.N_ab)                    
                else: 
                    a[e], p_a[e] = self.Random(ab[e], self.N_ab)
                         
        p_e = dict(p_a, **p_b)
         
        for e in set(ab.keys()).symmetric_difference(set(self.elements)):
            if (e=='H2') | (e=='He'):      
                b[e] = ab[e]
                p_b[e]= ' '
            else:
                a[e] = ab[e]  
                p_a[e]= ' '
        
        
        return a,b,p_a,p_b, p_e 
    
    def calculating_spectrum(self, a,b, pressures, temperature, gravity, MMW, modE):
            #print(a,b)
            atmosphere =  Radtrans(line_species = list(a.keys()), \
                          rayleigh_species = list(b.keys()), \
                          continuum_opacities = ['H2-H2', 'H2-He'], \
                          wlen_bords_micron = [self.wlmin, self.wlmax], mode= modE)

            abundances = a
            abundances.update(b)
            
            atmosphere.setup_opa_structure(pressures)
            atmosphere.calc_flux(temperature, abundances, gravity, MMW)
            fl= atmosphere.flux/1e-6
            wl= nc.c/atmosphere.freq/1e-4
            
            return wl, fl  
        
    def plotting_PTprofile(self, pressures, temperature, percent): 
        plt.figure(figsize=(30,15))
        plt.plot(temperature, pressures)
        plt.yscale('log')
        plt.ylim([1e2, 1e-6])
        plt.xlabel('T (K)', fontsize= 20)
        plt.ylabel('P (bar)', fontsize= 20)
                
        if not os.path.exists(self.spectrum_folder+'/PT/'): 
            os.system('mkdir '+ self.spectrum_folder+'/PT/')               ###### making the PT folder #######
            
        plt.title('T '+ str(percent) ,fontsize=20)
        plt.xticks(fontsize= 20)
        plt.yticks(fontsize= 20)
        PT_name= self.spectrum_folder+'/PT/T'+'_'+ str(percent) +'.png'
        plt.savefig(PT_name)
#         plt.show()
        plt.clf()
    
    def plot_title(self, p_a,p_b, abK): 
        
        p_b.update(p_a)     ### or p_a.update(p_b)- doesnt matter, we are sorting
        perct=np.sort(list(p_b.keys()))
        percentage = [' ['+str(p_b[p])+'%]' for p in perct]

        return ''.join(chain.from_iterable(zip(percentage, cycle(np.sort(abK)))))
    
    def plotting_spectrum(self,wl,fl,percent,i,p_a,p_b,p_e,abK): 
        
        e= np.sort(list(p_e.keys()))
        per = [' ['+str(int(float(p_e[p])))+'%]' for p in e]
        el= ''.join(chain.from_iterable(zip(per, cycle(np.sort(list(p_e.keys()))))))
        
        ##### saving pngs #####
        plt.figure(figsize=(30,15))
        plt.plot(wl, fl)
        
        if (len(p_a)+len(p_b)) ==0:
            plt.title('_'.join(abK)+' [T '+str(percent)+'%]',fontsize= 20)
            #print('title ', '_'.join(abK)+' [T '+str(percent)+'%]')

        else: 
            plt.title(self.plot_title(p_a,p_b,abK)+' [T '+str(percent)+'%]',fontsize=20)
            #print('title ',self.plot_title(p_a,p_b, abK)+' [T '+str(percent)+'%]')
            
        plt.xticks(fontsize= 20)
        plt.yticks(fontsize= 20)    
        plt.xscale('log')
        plt.xlabel('Wavelength (microns)', fontsize= 20)
        plt.ylabel(r'Planet flux $F_\nu$ (10$^{-6}$ erg cm$^{-2}$ s$^{-1}$ Hz$^{-1}$)', fontsize= 20)
        #print('/T'+ '_' + str(percent) +'_ab '+ ' '.join(self.elements)+ '_' +str(i)+'.png')
        spectrum_name= self.spectrum_folder+'/T'+ '_' + str(percent) +'_ab '+ el 
        plt.savefig(spectrum_name + '.png') #' '.join(self.elements)+ '_' +str(i)+
        #plt.show()
        plt.clf()
        

    def saving_spectrum(self, Spectrum, wl, fl, temperature, percent, a, p_a, b, p_b, s):   
        
        # with open(self.spectrum_folder+ '/spectrum.csv', mode='w+') as file:
        #     writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        #     writer.writerow(['T_eq= ', '1500','log g= ','1e1**2.45'])
        #     writer.writerow(['Wavelength (microns)', 'Planet Flux (10^-6 erg/cm2/s/Hz)'])
        #     for l in np.arange(len(wl)):
        #         writer.writerow([wl[l],fl[l]])

        Spectrum[int(s)] = {'wl': wl.tolist() , 
                       'fl': fl.tolist() ,
                       'T': temperature.tolist(), 
                       'Tp': percent, 
                       'LineSpecies': list(a), 
                       'LinesChange': p_a, 
                       'RayleighSpecies' : list(b),
                       'RayleighChange': p_b
                        }
        
        with open(self.spectrum_folder +'/spectrum.json','w+') as fp: 
            json.dump(Spectrum, fp, sort_keys=True, indent=4)

        return Spectrum
