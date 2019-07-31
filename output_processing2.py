# Return EHF from multiple simulation results of Operative Temperature

import glob
from multiprocessing import Pool
import os
import pandas as pd
from dict_update import update

def set_delta_T(n):
    
    if n < .25:
        delta_T = 0
    elif n < .5:
        delta_T = 1.2
    elif n < .75:
        delta_T = 1.8
    else:
        delta_T = 2.2
    
    return delta_T

def process_outputs(line, month_means, output_name,ach=True):
    
    df_temp = {
        'folder': [],
        'file': [],
        'zone': [],
        'temp': [],
        'temp_max': [],
        'ach': [],
        'ehf': []
    }
        
    print(line['file'],' ',line['folder'])  # , end='\r')
    
    csv_file = line['file'].split('.')[0]+'out.csv' 
    df = pd.read_csv(line['folder']+'/'+csv_file)
    
    delta_T = set_delta_T(line['v_ar'])
        
    if line['file'][0] == 'w':
        n_zones = 6 
        
        for zn in range(n_zones):
            
            df_temp['file'].append(line['file'].split('.')[0])
            df_temp['folder'].append(line['folder'])
            df_temp['zone'].append(zn) 

            df_temp['temp'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
            df_temp['temp_max'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).max())
            if ach:
                df_temp['ach'].append((df['OFFICE_'+'{:02.0f}'.format(zn)+':AFN Zone Infiltration Air Change Rate [ach](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
            else:
                df_temp['ach'].append(0)
            
            df['E_hot'] = -1
            df['sup_lim'] = month_means['mean_temp'] + 3.5 + delta_T
            df.loc[df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'] > df['sup_lim'], 'E_hot'] = 1
            df.loc[df['OFFICE_'+'{:02.0f}'.format(zn)+':Zone Operative Temperature [C](Hourly)'] <= df['sup_lim'], 'E_hot'] = 0
            
            df_temp['ehf'].append(df['E_hot'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean())
    else:
        
        df_temp['file'].append(line['file'].split('.')[0])
        df_temp['folder'].append(line['folder'])
        df_temp['zone'].append(line['file'].split('.')[0][-1])

        df_temp['temp'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
        df_temp['temp_max'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).max())
        if ach:
            df_temp['ach'].append((df['OFFICE:AFN Zone Infiltration Air Change Rate [ach](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())
        else:
            df_temp['ach'].append(0)
            
        df['E_hot'] = -1
        df['sup_lim'] = month_means['mean_temp'] + 3.5 + delta_T
        df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] > df['sup_lim'], 'E_hot'] = 1
        df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] <= df['sup_lim'], 'E_hot'] = 0
            
        df_temp['ehf'].append(df['E_hot'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean())
    
    return(df_temp)

def main(df_base, month_means, output_name, ach=True):
    
    df_final = {
        'folder': [],
        'file': [],
        'zone': [],
        'temp': [],
        'temp_max': [],
        'ach': [],
        'ehf': []
    }
    
    MONTH_MEANS = pd.read_csv(month_means)
    num_cluster = len(df_base['folder'].unique())
    
    p = Pool(num_cluster)
    result_map = p.starmap(process_outputs, zip(
        # [df_base.query('folder == "cluster'+str(i)+'"') for i in range(num_cluster)],
        [df_base.iloc[i] for i in range(len(df_base))],
        [MONTH_MEANS for _ in range(len(df_base))],
        [output_name for _ in range(len(df_base))],
        [ach for _ in range(len(df_base))]
    ))
    p.close()
    p.join()
    for df_temp in result_map:
        for key in df_final.keys():
            for i in range(len(df_temp[key])):
                df_final[key].append(df_temp[key][i])
    
    # df_final = pd.DataFrame(df_final)
    # df_final = pd.concat([df_base, df_final], axis=1, ignore_index=True)
    df_output = pd.DataFrame(df_final)
    df_output.to_csv(output_name+'.csv', index=False)
    print('\tDone processing!')

# df_base = pd.read_csv('test.csv')
# os.chdir('test')
# main(df_base, '/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv', 'teste')
