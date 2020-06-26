# data_filename= creating_json(ab1)

from Pspectra.retrieveSpectrum.retrieveSpectrum import retrieve_spectrum 

data_filename = 'sample_file.json' 
elements =[] 

Spec = retrieve_spectrum(data_folder='Pspectra/', data_filename= data_filename, \
        N_temp= 1 , state_T= 'None' ,  \
        elements= elements, N_ab=1, state_ab='None',\
        spectrum_folder ='/home/malavika/Documents/petitRT/spectrum_codeastro/',\
        delta = 20 , wlmin = 0.3 , wlmax= 15)

Spec. Nspectra() 