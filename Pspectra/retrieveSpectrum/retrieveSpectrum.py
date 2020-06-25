

class retreive_spectrum: 
    
    def __init__(self, data_folder, data_filename, N_temp, state_T, elements, N_ab, state_ab,\
                 spectrum_folder, delta, wlmin, wlmax ): 
        
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
        
        self.spectrum=Spectrum(self.N_temp, self.state_T, self.elements,self.N_ab, self.state_ab,\
                               self.spectrum_folder, self.delta, self.wlmin, self.wlmax)
        
        
    def obtaining_data(self):

        MMW= self.parameters['MMW']
        ab= self.parameters['ab']
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
    
    def Nspectra(self): 
    
        pressures, temperature, abundances, gravity, MMW = self.obtaining_data()
        abK= list(abundances.keys())
        
        for j in np.arange(self.N_temp):         #### Temperature variations #### 
            
            temperature, percent = self.spectrum.varyingT(temperature, j) 
            #print(temperature)
            for i in np.arange(self.N_ab):      #### Abundance variations #### 
                
                    a,b,p_a,p_b, p_e= self.spectrum.varyingAbundance(abundances, i) ##finding abundances #####                          
                    print(a,b)
                    wl, fl= self.spectrum.calculating_spectrum(a, b, pressures, temperature, gravity, MMW)  ##calculating spectrum ######

                    #saving the spectrum 
                    self.spectrum.saving_spectrum(wl,fl)
                    
#                     print(j,i, 'percent ', percent)
                    
                    
                    #plotting and saving 
#                     self.spectrum.plotting_PTprofile(pressures, temperature, percent)
#                     self.spectrum.plotting_spectrum(wl,fl,percent,i, p_a,p_b, p_e, abK)
                    
                    