
import glob
import json
import os

def main():
    FOLDER_STDRD = 'cluster'
    REST = {
        '015': .15  # ,
        # '020': .2,
        # '030': .3,
        # '040': .4,
        # '050': .5
    }
    os.chdir('crack')
    for i in range(10):
        os.chdir(FOLDER_STDRD+str(i))
        
        epjson_files = sorted(glob.glob('010*.epJSON')) 
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
                
                with open(crack+f[3:], 'w') as file:
                    file.write(json.dumps(model))
            
        os.chdir('..')
        
main()
