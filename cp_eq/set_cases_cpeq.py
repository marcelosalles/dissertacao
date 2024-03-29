import collections
import json
import os
import pandas as pd
from pyDOE import lhs

from idf_creator_floor import main_whole
from singlezone_diss import main

def update(d, u):
    # Function to update dictionaries
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

SAMPLE_SIZE = 1000
SAMPLE_NAME = 'sample_cpeq.csv'
N_CLUSTERS = 10

FOLDER = 'cpeq'
NAME_STDRD = 'whole'
NAME_STDRD_2 = 'single'

# os.system('mkdir '+FOLDER)
# for i in range(N_CLUSTERS):
    # os.system('mkdir '+FOLDER+'/cluster'+str(i))

samples_x_cluster = SAMPLE_SIZE/N_CLUSTERS

# parameters = [
    # 'area',
    # 'ratio',
    # 'zone_height',
    # 'azimuth',
    # 'absorptance',
    # 'wall_u',
    # 'wall_ct',
    # 'wwr',
    # 'people',
    # 'corner_window',
    # 'open_fac',
    # 'floor_height'
# ]

# sample = lhs(len(parameters),SAMPLE_SIZE)

# samp_dict = {}

# for param in parameters:
    # samp_dict[param] = []

samp_dict = pd.read_csv(SAMPLE_NAME)


line = 0
# for bldg in sample:
for i in range(len(samp_dict['area'])):
    
    # for i in range(len(parameters)):
        # samp_dict[parameters[i]].append(bldg[i])
    
    area = 20+80*samp_dict['area'][i]  # [-1]
    ratio = .5+1.5*samp_dict['ratio'][i]  # [-1]
    zone_height = 2.4+.8*samp_dict['zone_height'][i]  # [-1]
    azimuth = 360*samp_dict['azimuth'][i]  # [-1]
    absorptance = .3+.6*samp_dict['absorptance'][i]  # [-1]
    wall_u = .5+3.9*samp_dict['wall_u'][i]  # [-1]
    wall_ct = 20+380*samp_dict['wall_ct'][i]  # [-1]
    wwr = .1+.5*samp_dict['wwr'][i]  # [-1]
    people = .05+.45*samp_dict['people'][i]  # [-1]
    open_fac = .1+.9*samp_dict['open_fac'][i]  # [-1]
    floor_height = 30*samp_dict['floor_height'][i]  # [-1]
    
    if samp_dict['corner_window'][i] > .5:  # [-1]
        corner_window = False
    else:
        corner_window = True
    
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
        zone_feat['open_fac'].append(open_fac)
        zone_feat['glass'].append(.87)
    
    cluster_n = int(line//samples_x_cluster)
    
    caso = '{:04.0f}'.format(line)
    output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD+'_{}.epJSON'.format(caso))

    # main_whole(zone_area = area, zone_ratio = ratio, zone_height = zone_height, absorptance = absorptance, shading = 0, azimuth = azimuth,
        # corr_width = corr_width, wall_u = wall_u, wall_ct=wall_ct, corr_vent = 1, stairs = 0, zone_feat = zone_feat, concrete_eps=True,
        # zones_x_floor = 6, n_floors = 1, corner_window=corner_window, ground=False, roof=False, floor_height = 15,
        # input_file = "seed_single.json",output = output)
    
    azimuth_left = (azimuth+270)%360
    azimuth_right = (azimuth+90)%360
    
    for i in range(6):
        if i%2 == 0:
            azi = azimuth_left
        else:
            azi = azimuth_right
            
        output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD_2+'_{}_'.format(caso)+str(i)+'.epJSON')
        main(zone_area=area, zone_ratio=ratio, zone_height=zone_height, absorptance=absorptance,
        shading=0, azimuth=azi, bldg_ratio=1, wall_u=wall_u, wall_ct=wall_ct,
        zn=i, floor_height=floor_height, corner_window=corner_window, ground=0, roof=0, 
        people=people, glass_fs=.87, wwr=wwr, door=False, cp_eq=True, open_fac=open_fac,
        input_file='seed_single_U-conc-eps.json' , output=output)
    
    line += 1

# samp_df = pd.DataFrame(samp_dict)
# samp_df.to_csv(SAMPLE_NAME)
    
'''

'''
