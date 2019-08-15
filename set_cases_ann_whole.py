
import datetime
import json
import os
import pandas as pd

import dict_update
import sample_gen
import idf_creator_floor as whole_gen
import singlezone_diss
import runep_subprocess
import output_processing
import other_crack_fac

update = dict_update.update

# Globals
FOLDER = 'ann_whole'  #  'ann_whole_test'  # 'ann_whole_validation'  # 
SIZE =  20000  # 20000  # 155648
OUTPUT_NAME = 'sample_ann_whole'  # 'sample_ann_whole_test'  # 'sample_ann_whole_validation'  # 
NUM_CLUSTERS = int(os.cpu_count()/2)
# NAME_STDRD = 'whole'
NAME_STDRD_2 = 'single'
INPUT = "seed.json"  # INPUT_WHOLE 
# INPUT_SZ = "seed_sz.json"
EXTENSION = 'epJSON'
REMOVE_ALL_BUT = [EXTENSION, 'csv', 'err']
EPW_NAME = '~/dissertacao/BRA_SP_Sao.Paulo-Congonhas.AP.837800_TMYx.2003-2017.epw'
MONTH_MEANS = '/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv'
OUTPUT_PROCESSED = 'means_'+FOLDER
CONCRETE_EPS = True
SOBOL =  False  # True
# CRACK = .8

PARAMETERS = {
    'open_fac':[0.2,1],
    'v_ar':[0,1],
    'room_type':[0,1],
    'area':[20,100],
    'people':[.05,.2],
    'floor_height':[0,50],
    'roof':[0,1],
    'shading':[0,80],
    'ground':[0,1],
    'wall_u':[.5,4.4],
    'absorptance':[.2,.8],
    'glass':[.2,.87],
    'azimuth':[0,359.9],
    'wwr':[.1,.6],
    # 'corner_window':[0,1],  #####
    # 'n_floor':[1,9],        #####
    # 'ratio':[.4,2.5],
    # 'zone_height':[2.3,3.2],
    # 'wall_ct':[.22,450],
    # 'bldg_ratio': [.2,1]
}
        
start_time = datetime.datetime.now()

# Dependents
col_names = list(PARAMETERS)
samples_x_cluster = SIZE/NUM_CLUSTERS
name_length = '{:0'+str(len(str(SIZE)))+'.0f}'
name_length_cluster = '{:0'+str(len(str(NUM_CLUSTERS)))+'.0f}'

def add_crack(file_name, crack_fac=.1):
    
    with open(file_name, 'r') as file:            
        model = json.loads(file.read())
    model["AirflowNetwork:MultiZone:Surface:Crack"] = {
        "door_crack": {
            "air_mass_flow_coefficient_at_reference_conditions": crack_fac,
            "air_mass_flow_exponent": 0.667,
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 4
        }
    }
    
    with open(file_name, 'w') as file:
        file.write(json.dumps(model))

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
    
    if model_values['roof'] > .8:
        roof = True
    else:
        roof = False
        
    if model_values['ground'] > .85:
        ground = True
    else:
        ground = False
        
    if model_values['corner_window'] > .5:
        corner_window = True
    else:
        corner_window = False

    zone_feat = whole_gen.zone_list(model_values)
    
    cluster_n = int(line//samples_x_cluster)
    
    case = name_length.format(line)
    
    output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD+'_{}.epJSON'.format(case))
    df = df.append(pd.DataFrame([sample_line+['cluster'+'{:01.0f}'.format(cluster_n),NAME_STDRD+'_{}.epJSON'.format(case)]],columns=col_names+['folder','file']))
    print(output)
    whole_gen.main(
        zone_area = model_values['area'],
        zone_ratio = 1,  # model_values['ratio'],
        zone_height = 2.5,  # model_values['zone_height'],
        absorptance = model_values['absorptance'],
        shading = model_values['shading'],
        azimuth = model_values['azimuth'],
        corr_width = corr_width,
        wall_u = model_values['wall_u'], 
        wall_ct = 80.5,  # model_values['wall_ct'], 
        corr_vent = 1, 
        stairs = 0, 
        zone_feat = zone_feat, 
        concrete_eps=CONCRETE_EPS,
        zones_x_floor = 6, 
        n_floors = 1, 
        corner_window=corner_window, 
        ground=ground, 
        roof=roof, 
        floor_height = model_values['floor_height'],
        input_file = INPUT,
        output = output
    )
        
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
   
########################################################################

# Globals
FOLDER = 'ann_whole_validation'  #  'ann_whole_test'  # 'ann_whole_validation'  # 
SIZE =  5000  # 20000  # 155648
OUTPUT_NAME = 'sample_ann_whole_validation'  # 'sample_ann_whole'  # 'sample_ann_whole_test'  # 
NUM_CLUSTERS = int(os.cpu_count()/2)
# NAME_STDRD = 'whole'
NAME_STDRD_2 = 'single'
INPUT = "seed.json"  # INPUT_WHOLE 
# INPUT_SZ = "seed_sz.json"
EXTENSION = 'epJSON'
REMOVE_ALL_BUT = [EXTENSION, 'csv', 'err']
EPW_NAME = '~/dissertacao/BRA_SP_Sao.Paulo-Congonhas.AP.837800_TMYx.2003-2017.epw'
MONTH_MEANS = '/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv'
OUTPUT_PROCESSED = 'means_'+FOLDER
CONCRETE_EPS = True
SOBOL =  False  # True
# CRACK = .8

PARAMETERS = {
    'open_fac':[0.2,1],
    'v_ar':[0,1],
    'room_type':[0,1],
    'area':[20,100],
    'people':[.05,.2],
    'floor_height':[0,50],
    'roof':[0,1],
    'shading':[0,80],
    'ground':[0,1],
    'wall_u':[.5,4.4],
    'absorptance':[.2,.8],
    'glass':[.2,.87],
    'azimuth':[0,359.9],
    'wwr':[.1,.6],
    # 'corner_window':[0,1],  #####
    # 'n_floor':[1,9],        #####
    # 'ratio':[.4,2.5],
    # 'zone_height':[2.3,3.2],
    # 'wall_ct':[.22,450],
    # 'bldg_ratio': [.2,1]
}
        
start_time = datetime.datetime.now()

# Dependents
col_names = list(PARAMETERS)
samples_x_cluster = SIZE/NUM_CLUSTERS
name_length = '{:0'+str(len(str(SIZE)))+'.0f}'
name_length_cluster = '{:0'+str(len(str(NUM_CLUSTERS)))+'.0f}'

def add_crack(file_name, crack_fac=.1):
    
    with open(file_name, 'r') as file:            
        model = json.loads(file.read())
    model["AirflowNetwork:MultiZone:Surface:Crack"] = {
        "door_crack": {
            "air_mass_flow_coefficient_at_reference_conditions": crack_fac,
            "air_mass_flow_exponent": 0.667,
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 4
        }
    }
    
    with open(file_name, 'w') as file:
        file.write(json.dumps(model))

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
    
    if model_values['roof'] > .8:
        roof = True
    else:
        roof = False
        
    if model_values['ground'] > .85:
        ground = True
    else:
        ground = False
        
    if model_values['corner_window'] > .5:
        corner_window = True
    else:
        corner_window = False

    zone_feat = whole_gen.zone_list(model_values)
    
    cluster_n = int(line//samples_x_cluster)
    
    case = name_length.format(line)
    
    output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD+'_{}.epJSON'.format(case))
    df = df.append(pd.DataFrame([sample_line+['cluster'+'{:01.0f}'.format(cluster_n),NAME_STDRD+'_{}.epJSON'.format(case)]],columns=col_names+['folder','file']))
    print(output)
    whole_gen.main(
        zone_area = model_values['area'],
        zone_ratio = 1,  # model_values['ratio'],
        zone_height = 2.5,  # model_values['zone_height'],
        absorptance = model_values['absorptance'],
        shading = model_values['shading'],
        azimuth = model_values['azimuth'],
        corr_width = corr_width,
        wall_u = model_values['wall_u'], 
        wall_ct = 80.5,  # model_values['wall_ct'], 
        corr_vent = 1, 
        stairs = 0, 
        zone_feat = zone_feat, 
        concrete_eps=CONCRETE_EPS,
        zones_x_floor = 6, 
        n_floors = 1, 
        corner_window=corner_window, 
        ground=ground, 
        roof=roof, 
        floor_height = model_values['floor_height'],
        input_file = INPUT,
        output = output
    )
        
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
   
