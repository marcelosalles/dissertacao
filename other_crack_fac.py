
import glob
import json
import pandas as pd
import os

def main(df, folder='cpeq', num_clusters=10, pattern='_10_'):
    FOLDER_STDRD = 'cluster'
    name_length_cluster = '{:0'+str(len(str(num_clusters)))+'.0f}'
    REST = {
        '00': .005  # ,
        # '01': .01,
        # '10': .1,
        # '15': .15,
        # '20': .2,
        # '30': .3,
        # '45': .45,
        # '40': .4,
        # '50': .5,
        # '55': .55,
        # '60': .60,
        # '70': .70,
        # '80': .80,
        # '90': .90,
        # '95': .95,
        # '99': 1
    }
    df_out = df
    os.chdir(folder)
    for i in range(num_clusters):
        
        os.chdir(FOLDER_STDRD+name_length_cluster.format(i))
        
        epjson_files = sorted(glob.glob('single*.epJSON')) 
        # print(len(epjson_files))
        
        for f in epjson_files:
                
            with open(f, 'r') as file:            
                model = json.loads(file.read())
            
            for crack in REST.keys():
                model["AirflowNetwork:MultiZone:Surface:Crack"] = {
                    "door_crack": {
                        "air_mass_flow_coefficient_at_reference_conditions": REST[crack],
                        "air_mass_flow_exponent": 0.667,
                        "idf_max_extensible_fields": 0,
                        "idf_max_fields": 4
                    }
                }
                
                file_name = f.replace(pattern,'_'+crack+'_')
                new_line = pd.DataFrame(df.loc[df['file'] == f],columns=df.columns)
                new_line['file'] = file_name
                print(file_name)
                
                df_out = df_out.append(new_line)
                with open(file_name, 'w') as file:
                    file.write(json.dumps(model))
            
        os.chdir('..')
    os.chdir('..')
    
    return(df_out)

# main()
