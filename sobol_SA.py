import json
import numpy as np
import pandas as pd
from SALib.analyze import sobol
from SALib.sample import saltelli

# Global variables

BASE_DIR = '/home/marcelo/dissertacao'
# DATASET = 'dataset_12-20.csv'
N_CLUSTERS = 10

COL_NAMES = ['area', 'ratio', 'zone_height', 'abs', 'shading', 'azimuth',  # 
	'wall_u', 'wall_ct', 'wwr', 'open_fac', 'people',  'thermal_loads', 
    'glass', 'floor_height', 'bldg_ratio', 'room_type', 'ground', 'roof']  # 18 items.

BOUNDS = [-1, 1]

SIMULATIONS = 99978

def n_calc(d, n_cases, scnd_order = False):
    # N calculator
    
    if scnd_order:
        n_size = n_cases/(2*d + 2)
    else:
        n_size = n_cases/(d + 2)

    print(n_size)

    return int(n_size)


if __name__ == "__main__":

    # Define the model inputs

    cases = SIMULATIONS
    
    problem = {
        'num_vars': len(COL_NAMES),
        'names': COL_NAMES,
        'bounds': [BOUNDS for x in range(len(COL_NAMES))]
    }

    n_size = n_calc(problem['num_vars'], cases, scnd_order = True)
    
    #### SA
    
    for i in range(N_CLUSTERS):
        if i == 0:
            df_out = pd.read_csv('sobol/cluster0/means_cluster0.csv')
        else:
            df_out = df.append(pd.read_csv('sobol/cluster'+str(i)+'/means_cluster'+str(i)+'.csv'))

    df_out = df_out.sort_values(by=['file']) 
    # df_out = pd.read_csv(BASE_DIR+'/'+DATASET)
    
    print('EHF')
    Y = np.array(df_out['ehf'])
    sa = sobol.analyze(problem, Y, print_to_console=True)

    #### SA TEMP and ACH

    #temp
    print('TEMP')
    Y = np.array(df_out['temp'])
    sa = sobol.analyze(problem, Y, print_to_console=True)

    #ach
    print('ACH')
    Y = np.array(df_out['ach'])
    sa = sobol.analyze(problem, Y, print_to_console=True)
