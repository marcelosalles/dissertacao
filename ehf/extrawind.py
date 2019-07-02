import pandas as pd

FOLDER = 'sobol'
MONTH_MEANS = pd.read_csv('/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv')

def means(file_name, delta_T): 
    
    file_df = pd.read_csv(file_name)
    
    file_df['E_hot'] = -1
    file_df['sup_lim'] = MONTH_MEANS['mean_temp'] + 3.5 + delta_T
    file_df.loc[file_df['OFFICE:Zone Operative Temperature [C](Hourly)'] > file_df['sup_lim'], 'E_hot'] = 1
    file_df.loc[file_df['OFFICE:Zone Operative Temperature [C](Hourly)'] <= file_df['sup_lim'], 'E_hot'] = 0
    
    ehf = file_df['E_hot'][file_df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean()
    
    return ehf

def set_delta_T(n):
    
    if n > -.5 and n <= 0:
        delta_T = 1.2
    elif n > 0 and n <= .5:
        delta_T = 1.8
    else:
        delta_T = 2.2
    
    return delta_T

df = pd.read_csv(FOLDER+'/sample_results.csv')

for row in range(df.shape[0]):
    
    if df['thermal_loads'][row] > -.5:
    
        file_name = FOLDER+'/'+df['folder'][row]+'/'+df['file'][row]+'out.csv'
        
        delta_T = set_delta_T(df['thermal_loads'][row])
        
        ehf = means(file_name, delta_T)
        
        df['ehf'][row] = ehf
    
        print(file_name, end='\r')

df.to_csv(FOLDER+'/sample_results_fixed.csv')
