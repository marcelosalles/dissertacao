
import glob
import json
import os

def main(folder='cp_eq', num_clusters=10):
    FOLDER_STDRD = 'cluster'
    REST = {
        # '10': .1,
        '15': .15  # ,
        '20': .2,
        '30': .3,
        # '40': .4,
        '50': .5
    }
    os.chdir(folder)
    for i in range(num_clusters):
        os.chdir(FOLDER_STDRD+str(i))
        
        epjson_files = sorted(glob.glob('single*.epJSON')) 
        print(len(epjson_files))
        
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
                file_name = f.replace('_10_','_'+crack+'_')
                with open(file_name, 'w') as file:
                    file.write(json.dumps(model))
            
        os.chdir('..')
        
main()
