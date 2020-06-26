import json


def creating_json(ab1): 

    parameters = {}

    parameters['ab']= ab1
    parameters['MMW']= 2.33
    parameters['P0']= 0.01
    parameters['Rpl']=1.838
    parameters['pmin']= -6
    parameters['pmax']= 2
    parameters['R']= 100
    parameters['g']= 1e1**2.45
    parameters['kappa_IR']= 0.01
    parameters['gamma']= 0.4
    parameters['T_int']= 200.
    parameters['T_equ']= 1500.

    k= '_'.join(list(ab1.keys()))
    with open('Data/' + k + '.json','w+') as fp: 
        json.dump(parameters, fp, sort_keys=True, indent=4)
    
    return k + '.json'