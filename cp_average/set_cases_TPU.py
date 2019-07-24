from idf_creator_floor import main_whole
import json
from pyDOE import lhs
import pandas as pd

SAMPLE_SIZE = 1000
SAMPLE_NAME = 'sample_TPU.csv'
N_CLUSTERS = 10

FOLDER = 'TPU'
NAME_STDRD = 'average'
NAME_STDRD_TPU = 'tpu'

samples_x_cluster = SAMPLE_SIZE/N_CLUSTERS

sample = lhs(7,SAMPLE_SIZE)

samp_dict = {
    'area': [],
    'zone_height': [],
    'azimuth': [],
    'wall_u': [],
    'wwr': [],
    'people': [],
    'nfloor': []
}


line = 0
for bldg in sample:
    
    samp_dict['area'].append(bldg[0])
    samp_dict['zone_height'].append(bldg[1])
    samp_dict['azimuth'].append(bldg[2])
    samp_dict['wall_u'].append(bldg[3])
    samp_dict['wwr'].append(bldg[4])
    samp_dict['people'].append(bldg[5])
    samp_dict['nfloor'].append(bldg[6])
    
    area = 20+80*bldg[0]
    zone_height = 2.4+.8*bldg[1]
    azimuth = 360*bldg[2]
    wall_u = .5+3.9*bldg[3]
    wwr = .1+.5*bldg[4]
    people = .05+.45*bldg[5]
    nfloor = int(1+8*bldg[6])
    
    corr_width = 2
    
    ratio = area / ( ( 2 * corr_width + ( 4 * corr_width**2 + 48 * area )**(1/2) ) / 6 )**2
    
    # print(( 3 * (area/ratio)**(1/2) ) / ( 2 + 2 * ( area / (area/ratio)**(1/2) )))

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
    output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD+'_{}.epJSON'.format(caso))

    main_whole(zone_area = area, zone_ratio = ratio, zone_height = zone_height, absorptance = .5, shading = 0, azimuth = azimuth,
        corr_width = corr_width, wall_u = wall_u, wall_ct=150, corr_vent = 1, stairs = 0, zone_feat = zone_feat, concrete_eps=True,
        zones_x_floor = 6, n_floors = 1, corner_window=True, ground=False, roof=False, floor_height = nfloor*zone_height,
        input_file = "seed_single.json",output = output)

    with open(output, 'r') as file:
        average_model = json.loads(file.read())
        
    for surface in average_model["AirflowNetwork:MultiZone:Surface"].keys():
        if average_model["AirflowNetwork:MultiZone:Surface"][surface]["leakage_component_name"] == "Janela":
            average_model["AirflowNetwork:MultiZone:Surface"][surface]["external_node_name"] = average_model["AirflowNetwork:MultiZone:Surface"][surface]["surface_name"]+'_Node'

    with open('tpu_floor'+str(nfloor-1)+'.json', 'r') as file:
        tpu_cp = json.loads(file.read())

    complete_model = update(average_model, tpu_cp)
    output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD_TPU+'_{}.epJSON'.format(caso))
    
    with open(output, 'w') as file:
        file.write(json.dumps(complete_model))
    
    line += 1

samp_df = pd.DataFrame(samp_dict)
samp_df.to_csv(SAMPLE_NAME)
    
'''
'''
