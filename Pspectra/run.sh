ab1= {'H2': 0.74, 'He': 0.24,'CO_all_iso': 0.01} #, 'CO_all_iso': 0.01,'CO2': 0.00001,'CH4':0.000001, 'Na': 0.00001, 'K': 0.000001}
elements = []
data_filename= creating_json(ab1)

Spec = retreive_spectrum(data_folder='Data/', data_filename= data_filename, \
          N_temp= 1 , state_T= 'None',\  #random, toggle
          elements= elements, N_ab=1, state_ab='None',\
          spectrum_folder ='/home/malavika/Documents/petitRT/spectrum/',\
          delta = 20 , wlmin = 0.3 , wlmax= 15)


#no of spectra = N_temp * N_ab