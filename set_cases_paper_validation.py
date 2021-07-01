
import datetime
import json
import os
import pandas as pd

import dict_update
import sample_gen
import idf_creator as whole_gen
import runep_subprocess
import output_processing

update = dict_update.update

# Globals
FOLDER = 'paper_validation'
SIZE =  10
OUTPUT_NAME = 'sample_paper_validation'
NUM_CLUSTERS = 18  # int(os.cpu_count()/2)
NAME_STDRD = 'whole'
INPUT = "seed.json"  # INPUT_WHOLE 
EXTENSION = 'epJSON'
REMOVE_ALL_BUT = [EXTENSION, 'csv', 'err']
EPW_NAME = '~/dissertacao/BRA_SP_Sao.Paulo-Congonhas.AP.837800_TMYx.2003-2017.epw'
MONTH_MEANS = '/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv'
OUTPUT_PROCESSED = 'means_'+FOLDER
CONCRETE_EPS = False
SOBOL =  False  # True

ZONES_X_FLOOR = 6
N_FLOORS = 3

PARAMETERS = {
    'open_fac':[0.2,1],
    'v_ar':[0,1],
    'corner_window':[0,1],  #####
    # 'room_type':[0,1],
    'area':[20,100],
    'people':[.05,.2],
    # 'floor_height':[0,50],
    # 'roof':[0,1],
    'shading':[0,80],
    # 'ground':[0,1],
    # 'wall_u':[.5,4.4],
    'absorptance':[.2,.8],
    'glass':[.2,.87],
    'azimuth':[0,359.9],
    'wwr':[.1,.6],
    # 'n_floor':[1,9],        #####
    'ratio':[.4,2.5],
    'zone_height':[2.3,3.2],
    # 'wall_ct':[.22,450],
    # 'bldg_ratio': [.2,1]
    'wall_type': [0,1]
}

walls = {
    'par1': {
        'nome': 'concreto',
        'wall_u': 17.5,
        'wall_ct': 220,
        'file': 'par_1.json'
    },
    'par2a': {
        'nome': 'alvenaria',
        'wall_u': 3.962,
        'wall_ct': 138.272,
        'file': 'par_2.json'
    },
    'par2b': {
        'nome': 'meia_alvenaria',
        'wall_u': 3.962,
        'wall_ct': 69.136,
        'file': 'par_2.json'
    },
    'par3': {
        'nome': 'leve',
        'wall_u': .773,
        'wall_ct': 29.7875,
        'file': 'par_3.json'
    }
}
        
start_time = datetime.datetime.now()

# Dependents
col_names = list(PARAMETERS)
samples_x_cluster = SIZE/NUM_CLUSTERS
name_length = '{:0'+str(len(str(SIZE)))+'.0f}'
name_length_cluster = '{:0'+str(len(str(NUM_CLUSTERS)))+'.0f}'

def parameter_value(key, i):
    value = PARAMETERS[key][0]+(PARAMETERS[key][1]-PARAMETERS[key][0])*i
    return value

print('\nCREATING DIRECTORIES\n')

os.system('mkdir '+FOLDER)
for i in range(NUM_CLUSTERS):
    os.system('mkdir '+FOLDER+'/cluster'+name_length_cluster.format(i))
    
# Generate sample
print('\nGENERATING SAMPLE\n')

sample = sample_gen.main(SIZE, col_names, OUTPUT_NAME, sobol=SOBOL)
# sample = pd.read_csv(OUTPUT_NAME+'.csv')
if SOBOL:
    sample = (sample+1)/2

# Set cases
print('\nGENERATING MODELS\n')

df = pd.DataFrame(columns=col_names+['folder','file'])
line = 0
for i in range(len(sample)):
    
    sample_line = list(sample.iloc[i])
    
    model_values = dict((param,parameter_value(param, sample.loc[i, param])) for param in col_names)
    
    corr_width = 2
        
    if model_values['corner_window'] > .5:
        corner_window = True
    else:
        corner_window = False
        
    if model_values['wall_type'] > .6667:
        par_file = 'parede_eq/par_1.json'
    elif model_values['wall_type'] > .3333:
        par_file = 'parede_eq/par_2.json'
    else:
        par_file = 'parede_eq/par_3.json'

    n_zones = ZONES_X_FLOOR*N_FLOORS  # 6 zones, 3 floors
    zone_feat = whole_gen.zone_list(model_values,n_zones)
    
    cluster_n = int(line//samples_x_cluster)
    
    case = name_length.format(line)
    
    output = (FOLDER+'/cluster'+name_length_cluster.format(cluster_n)+'/'+NAME_STDRD+'_{}'.format(case)+'.epJSON')
    df = df.append(pd.DataFrame([sample_line+['cluster'+name_length_cluster.format(cluster_n),NAME_STDRD+'_{}'.format(case)+'.epJSON'.format(case)]],columns=col_names+['folder','file']))
    print(output)
    whole_gen.main(
        zone_area = model_values['area'],
        zone_ratio = model_values['ratio'],  #1,  # 
        zone_height = model_values['zone_height'],  # 2.5,  # 
        absorptance = model_values['absorptance'],
        shading = model_values['shading'],
        azimuth = model_values['azimuth'],
        corr_width = corr_width,
        wall_u = 1, 
        wall_ct = 111,  # 80.5,  # 
        corr_vent = 1, 
        stairs = 0, 
        zone_feat = zone_feat, 
        concrete_eps=CONCRETE_EPS,
        zones_x_floor = ZONES_X_FLOOR, 
        n_floors = N_FLOORS, 
        corner_window=corner_window,  
        input_file = INPUT,
        output = output
    )

    with open(output, 'r') as file:
        model = json.loads(file.read())

    with open(par_file, 'r') as file:
        par_obj = json.loads(file.read())

    model = update(model, par_obj)
    
    with open(output, 'w') as file:
        file.write(json.dumps(model))
        
    line += 1

os.chdir(FOLDER)
print('\nRUNNING SIMULATIONS\n')
list_epjson_names = runep_subprocess.gen_list_epjson_names(NUM_CLUSTERS, EXTENSION)
runep_subprocess.main(list_epjson_names, NUM_CLUSTERS, EXTENSION, REMOVE_ALL_BUT, epw_name=EPW_NAME)

print('\nPROCESSING OUTPUT\n')
output_processing.main(df, MONTH_MEANS, OUTPUT_PROCESSED)

end_time = datetime.datetime.now()
total_time = (end_time - start_time)
print("Total processing time: " + str(total_time))
