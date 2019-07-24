# Return EHF from multiple simulation results of Operative Temperature

import argparse
import csv
import datetime
import glob
from multiprocessing import Pool
import os
import pandas as pd
import re

def process_folder(folder, month_means, output_name):
    
    line = 0
    
    os.chdir(folder)
    epjson_files = sorted(glob.glob('*.epJSON'))  
    df_temp = {
        'folder': [],
        'file': [],
        'zone': [],
        'temp': [],
        'temp_max': [],
        'ach': [],
        'ehf': []
    }
    
    for file in epjson_files:
        
        file_n = re.findall('\d+',file)[0]
        
        print(line,' ',file, end='\r')
        line += 1
        
        csv_file = file[:-7]+'out.csv' 
        df = pd.read_csv(csv_file)
        
        if file[0] == 'w':
            n_zones = 6 
            
            for zn in range(n_zones):
                
                df_temp['file'].append(file[:-7])
                df_temp['folder'].append(folder)
                df_temp['zone'].append(zn) 

                df_temp['temp'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
                df_temp['temp_max'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).max())
                if ach:
                    df_temp['ach'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':AFN Zone Infiltration Air Change Rate [ach](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
                else:
                     df_temp['ach'].append(0)
                df['E_hot'] = -1
                df['sup_lim'] = month_means['mean_temp'] + 3.5
                df.loc[df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'] > df['sup_lim'], 'E_hot'] = 1
                df.loc[df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'] <= df['sup_lim'], 'E_hot'] = 0
                
                df_temp['ehf'].append(df['E_hot'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean())
        else:
            
            df_temp['file'].append(file[:-7])
            df_temp['folder'].append(folder) 
            df_temp['zone'].append(file[-8:-7]) 

            df_temp['temp'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
            df_temp['temp_max'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).max())
            if ach:
                df_temp['ach'].append((df['OFFICE:AFN Zone Infiltration Air Change Rate [ach](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
            else:
                df_temp['ach'].append(0)
            df['E_hot'] = -1
            df['sup_lim'] = month_means['mean_temp'] + 3.5
            df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] > df['sup_lim'], 'E_hot'] = 1
            df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] <= df['sup_lim'], 'E_hot'] = 0
                
            df_temp['ehf'].append(df['E_hot'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean())
    
    df_output = pd.DataFrame(df_temp)
    df_output.to_csv(output_name+'_{}.csv'.format(folder), index=False)
    print('\tDone processing folder \'{}\''.format(folder))

def main(num_cluster, extension, month_means, output_name, ach=True):
    
    EXTENSION = extension
    MONTH_MEANS = pd.read_csv(month_means)
    folders = ['cluster'+str(i) for i in range(num_cluster)]
    
    p = Pool(num_cluster)
    p.starmap(process_folder, zip(folders,[MONTH_MEANS for _ in range(num_cluster)],[output_name for _ in range(num_cluster)]))

# os.chdir('cp_average')
# main(10, '.epJSON', '/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv', 'teste')
