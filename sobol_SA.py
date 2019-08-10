import json
import numpy as np
import pandas as pd
from SALib.analyze import sobol
from SALib.sample import saltelli

# Global variables

# BASE_DIR = '/home/marcelo/dissertacao'
BASE_DIR = '/media/marcelo/OS/dissertacao/sobol2'
DATASET = 'means_sobol2.csv'
N_CLUSTERS = 10

COL_NAMES = [
    'area',  # 20,100],
    'ratio',  # .4,2.5],
    'zone_height',  # 2.3,3.2],
    'azimuth',  # 0,359.9],
    'floor_height',  # 0,50],
    'absorptance',  # .2,.8],
    'wall_u',  # .5,4.4],
    'wall_ct',  # .22,450],
    'wwr',  # .1,.6],
    'glass',  # .2,.87],
    'shading',  # 0,80],
    'people',  # .05,.2],
    # 'corner_window',  # 0,1],
    'open_fac',  # 0.2,1],
    'roof',  # 0,1],
    'ground',  # 0,1],
    'bldg_ratio',  # .2,1],
    # 'n_floor',  # 1,9],
    'v_ar',  # 0,1],
    'room_type',  # 0,1]
    ]  # 18 items.

BOUNDS = [-1, 1]

SIMULATIONS = 155648  # 77824  # 99978

def print_indices(S, problem, calc_second_order, y):
    
    t = open(BASE_DIR+'/s1_'+y+'.csv','a')
    # Output to console
    if not problem.get('groups'):
        title = 'Parameter'
        names = problem['names']
        D = problem['num_vars']
    else:
        title = 'Group'
        _, names = compute_groups_matrix(problem['groups'])
        D = len(names)

    print('%s, S1, S1_conf, ST, ST_conf' % title, file = t)

    for j in range(D):
        print('%s, %f, %f, %f, %f' % (names[j], S['S1'][
            j], S['S1_conf'][j], S['ST'][j], S['ST_conf'][j]), file = t)
    t.close()

    if calc_second_order:
        t = open(BASE_DIR+'/s2_'+y+'.csv','a')
        print('%s_1, %s_2, S2, S2_conf' % (title, title), file = t)

        for j in range(D):
            for k in range(j + 1, D):
                print("%s, %s, %f, %f" % (names[j], names[k], 
                    S['S2'][j, k], S['S2_conf'][j, k]), file = t)
        t.close()

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
    
    # for i in range(N_CLUSTERS):
        # if i == 0:
            # df_out = pd.read_csv('sobol/cluster0/means_cluster0.csv')
        # else:
            # df_out = df_out.append(pd.read_csv('sobol/cluster'+str(i)+'/means_cluster'+str(i)+'.csv'))

    df_out = pd.read_csv(BASE_DIR+'/'+DATASET)
    df_out = df_out.sort_values('file')
    
    print('EHF')
    Y = np.array(df_out['ehf'])
    sa = sobol.analyze(problem, Y)  # , print_to_console=True)
    
    print_indices(sa, problem, True,'ehf')
        
    #### SA TEMP and ACH

    #temp
    print('TEMP')
    Y = np.array(df_out['temp'])
    sa = sobol.analyze(problem, Y)
    
    print_indices(sa, problem, True,'temp')

    #ach
    print('ACH')
    Y = np.array(df_out['ach'])
    sa = sobol.analyze(problem, Y)
    
    print_indices(sa, problem, True,'ach')
