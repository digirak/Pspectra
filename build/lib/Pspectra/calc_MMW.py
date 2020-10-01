def calc_MMW(abundances):

    MMWs = {}
    MMWs['H2'] = 2.
    MMWs['He'] = 4.
    MMWs['H2O'] = 18.
    MMWs['CH4'] = 16.
    MMWs['CO2'] = 44.
    MMWs['CO'] = 28.
    MMWs['Na'] = 23.
    MMWs['K'] = 39.
    MMWs['NH3'] = 17.
    MMWs['HCN'] = 27.
    MMWs['C2H2,acetylene'] = 26.
    MMWs['PH3'] = 34.
    MMWs['H2S'] = 34.
    MMWs['VO'] = 67.
    MMWs['TiO'] = 64.

    MMW = 0.
    for key in abundances.keys():
        if key == 'CO_all_iso':
            MMW += abundances[key]/MMWs['CO']
        elif key == 'CH4_main_iso':
            MMW += abundances[key]/MMWs['CH4']
        elif key == 'H2O_main_iso':
            MMW += abundances[key]/MMWs['H2O']
        else:
            MMW += abundances[key]/MMWs[key]
    
    return 1./MMW
