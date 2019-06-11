# Return EHF from multiple simulation results of Operative Temperature

import argparse
import csv
import datetime
import glob
from multiprocessing import Pool
import os
import pandas as pd

FOLDER_STDRD = 'cluster'
LEN_FOLDER_NAME = len(FOLDER_STDRD) +1
NUMBER_OF_DIGITS = 4  # ex. 0, 00, 000, 0000...
BASE_DIR = '/media/marcelo/OS/dissertacao/crack'
MONTH_MEANS = pd.read_csv('/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv')
MAX_THREADS = 10
OUTPUT = '015means'  # means

def process_folder(folder):
    
    line = 0
    folder_name = folder[len(folder)-LEN_FOLDER_NAME:]
    os.chdir(folder)  # BASE_DIR+'/'+
    
    # epjson_files = sorted(glob.glob('*.epJSON'))  
    epjson_files = sorted(glob.glob('015*.epJSON'))  
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
        
        file_n = int(file[len(file)-7-NUMBER_OF_DIGITS:len(file)-7])
        
        print(line,' ',file, end='\r')
        line += 1
        
        csv_file = file[:-7]+'out.csv' 
        df = pd.read_csv(csv_file)
        
        if file[0] == 'w':
            n_zones = 6 
            
            for zn in range(n_zones):
                
                df_temp['file'].append(file[:-7])
                df_temp['folder'].append(folder_name)
                df_temp['zone'].append(zn) 

                df_temp['temp'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
                df_temp['temp_max'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).max())
                df_temp['ach'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':AFN Zone Infiltration Air Change Rate [ach](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
                
                df['E_hot'] = -1
                df['sup_lim'] = MONTH_MEANS['mean_temp'] + 3.5
                df.loc[df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'] > df['sup_lim'], 'E_hot'] = 1
                df.loc[df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'] <= df['sup_lim'], 'E_hot'] = 0
                
                df_temp['ehf'].append(df['E_hot'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean())
        else:
            
            df_temp['file'].append(file[:-7])
            df_temp['folder'].append(folder_name) 
            df_temp['zone'].append(file[-8:-7]) 

            df_temp['temp'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
            df_temp['temp_max'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).max())
            df_temp['ach'].append((df['OFFICE:AFN Zone Infiltration Air Change Rate [ach](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
            
            df['E_hot'] = -1
            df['sup_lim'] = MONTH_MEANS['mean_temp'] + 3.5
            df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] > df['sup_lim'], 'E_hot'] = 1
            df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] <= df['sup_lim'], 'E_hot'] = 0
                
            df_temp['ehf'].append(df['E_hot'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean())
    
    df_output = pd.DataFrame(df_temp)
    df_output.to_csv(OUTPUT+'_{}.csv'.format(folder_name), index=False)
    print('\tDone processing folder \'{}\''.format(folder_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process output data from Energyplus.')
    parser.add_argument('-t',
                        action='store',
                        type=int,
                        help='runs T threads')

    args = parser.parse_args()

    folders = glob.glob(BASE_DIR+'/'+FOLDER_STDRD+'*')
   
    print('Processing {} folders in \'{}\':'.format(len(folders), BASE_DIR))
    for folder in folders:
        print('\t{}'.format(folder))

    start_time = datetime.datetime.now()

    if args.t:
        p = Pool(args.t)
        p.map(process_folder, folders)
    else:
        num_folders = len(folders)
        p = Pool(min(num_folders, MAX_THREADS))
        p.map(process_folder, folders)

    end_time = datetime.datetime.now()

    total_time = (end_time - start_time)
    
    print("Total processing time: " + str(total_time))

