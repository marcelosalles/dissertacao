import collections
from idf_creator_floor import main_whole
import json
import os
from pyDOE import lhs
import pandas as pd

def update(d, u):
    # Function to update dictionaries
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

SAMPLE_SIZE = 100
SAMPLE_NAME = 'sample_diss.csv'
N_CLUSTERS = 10

FOLDER = 'wall'
NAME_STDRD = 'epsconc'
NAME_STDRD_2 = 'refwall'  # wfg215

os.system('mkdir '+FOLDER)
for i in range(N_CLUSTERS):
    os.system('mkdir '+FOLDER+'/cluster'+str(i))

samples_x_cluster = SAMPLE_SIZE/N_CLUSTERS

parameters = [
    'area',
    'ratio',
    'zone_height',
    'azimuth',
    'absorptance',
    'wwr',
    'people'
]

sample = lhs(len(parameters),SAMPLE_SIZE)

samp_dict = {}

for param in parameters:
    samp_dict[param] = []

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

line = 0
for bldg in sample:
    
    for i in range(len(parameters)):
        samp_dict[parameters[i]].append(bldg[i])
    
    area = 20+80*bldg[0]
    zone_height = 2.4+.8*bldg[1]
    azimuth = 180*bldg[2]
    ratio = .5 + 1.5*bldg[3]
    wwr = .1+.5*bldg[4]
    people = .05+.45*bldg[5]
    absorptance = .3 + .6*bldg[6]
    
    # if bldg[7] < .25:
        # par = 'par1'
    # elif bldg[7] < .5:
        # par = 'par2a'
    # elif bldg[7] < .75:
        # par = 'par2b'NAME_STDRD_2
    # else:
        # par = 'par3'
    
    corr_width = 2
    
    zone_feat = {
        'people': [],
        'wwr': [],
        'open_fac': [],
        'glass': []
    }
    
    for i in range(6):
        zone_feat['people'].append(people)
        zone_feat['wwr'].append(wwr)
        zone_feat['open_fac'].append(1)
        zone_feat['glass'].append(.87)
    
    cluster_n = int(line//samples_x_cluster)
    
    caso = '{:04.0f}'.format(line)
    
    for par in walls.keys():        
        NAME = NAME_STDRD+'_'+par
        output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME+'_{}.epJSON'.format(caso))
        
        wall_u = walls[par]['wall_u']
        wall_ct = walls[par]['wall_ct']
        par_file = walls[par]['file']

        main_whole(zone_area = area, zone_ratio = ratio, zone_height = zone_height, absorptance = absorptance, shading = 0, azimuth = azimuth,
            corr_width = corr_width, wall_u = wall_u, wall_ct=wall_ct, corr_vent = 1, stairs = 0, zone_feat = zone_feat, concrete_eps=True,
            zones_x_floor = 6, n_floors = 1, corner_window=True, ground=False, roof=False, floor_height = 15,
            input_file = "seed_single.json",output = output)

        with open(output, 'r') as file:
            model_1 = json.loads(file.read())

        with open(par_file, 'r') as file:
            par_obj = json.loads(file.read())

        model_2 = update(model_1, par_obj)
        NAME2 = NAME_STDRD_2+'_'+par
        output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME2+'_{}.epJSON'.format(caso))
        
        with open(output, 'w') as file:
            file.write(json.dumps(model_2))
    
    line += 1

samp_df = pd.DataFrame(samp_dict)
samp_df.to_csv(SAMPLE_NAME,index=False)
    
'''
'''
