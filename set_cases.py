from singlezone_diss import main
import os
import pandas as pd

def main(sample_name, parameters, num_clusters, folder, sobol=False):
    
    os.system('mkdir '+folder)
    for i in range(num_clusters):
        os.system('mkdir '+folder+'/cluster'+str(i))
    
    # load samples
    sample = pd.read_csv(sample_name)
    samples_x_cluster = sample.shape[0]/num_clusters
    
    if sobol:
        sample = (sample+1)/2
         
    samp_dict = {}

    for param in parameters:
        samp_dict[param] = []

    # start iteration
    for line in range(sample.shape[0]):

        # prepare inputs
        area = sample['area'][line] * 
        ratio = sample['ratio'][line]
        zone_height = sample['zone_height'][line]
        azimuth = sample['azimuth'][line]
        absorptance = sample['abs'][line]
        wall_u = sample['wall_u'][line]
        wall_ct = sample['wall_ct'][line]
        shading = sample['shading'][line]
        wwr = sample['wwr'][line]
        open_fac = sample['open_fac'][line]
        people = sample['people'][line]
        glass = sample['glass'][line]
        floor_height = sample['floor_height'][line]
        bldg_ratio = sample['bldg_ratio'][line]
        
        if sample['room_type'][line] < -.6:
            room_type = '1_window'
            zn = 1
            corner_window = True
        elif sample['room_type'][line] < -.2:
            room_type = '3_window'
            zn = 0
            corner_window = True
        elif sample['room_type'][line] < .2:
            room_type = '1_wall'
            zn = 1
            corner_window = False
        elif sample['room_type'][line] < .6:
            room_type = '3_wall'
            zn = 0
            corner_window = False
        else:
            room_type = '0_window'
            zn = 2
            corner_window = False
        
        if sample['ground'][line] < 0:
            ground = 0
        else:
            ground = 1
            
        if sample['roof'][line] < 0:
            roof = 0
        else:
            roof = 1
        
        cluster_n = int(line//samples_x_cluster)
        
        caso = '{:05.0f}'.format(line)
        output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD+'_{}.epJSON'.format(caso))
        
        main(zone_area=area, zone_ratio=ratio, zone_height=zone_height,
        absorptance=absorptance, shading=shading, azimuth=azimuth,
        bldg_ratio=bldg_ratio, wall_u=wall_u, wall_ct=wall_ct,
        zn=zn, floor_height=floor_height, corner_window=corner_window,
        ground=ground, roof=roof, people=people, glass_fs=glass, wwr=wwr,
        door=False, cp_eq = True, open_fac=open_fac,
        input_file="seed_single_U-conc-eps.json", output=output)
