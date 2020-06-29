import numpy as np
import json

class Data: 
    
    def __init__(self, data_folder, data_filename): 
        self.filename= data_filename # 'values.json' / 'Molliere_without_clouds.json'
        self.folder = data_folder #'Data/'
        
    def json_to_dict(self):
        with open(self.folder+self.filename, 'r') as fp:
             ab = json.load(fp)
        return ab
    
    def check_valueORfile(self,dictionary): 
        c=0
        for key in dictionary: # loop through all the keys
            value = dictionary[key]   # get value for the key
            if np.size(value) > 1:   
                c+=1
        return c>1