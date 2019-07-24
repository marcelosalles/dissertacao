import datetime
import glob
from multiprocessing import Pool
import os
import pandas as pd

import other_crack_fac
import runep_subprocess
import set_cases_crack
import temp_ach_multiprocess_cpeq

num_clusters = int(os.cpu_count()/2)

set_cases_crack.set_cases()

os.chdir('crack')
other_crack_fac.main()

### Mudar caso necessario
extension = 'epJSON'
version_EnergyPlus = 'energyplus-8.9.0'
remove_all_but = ['.'+extension, '.csv']  # 'Table.csv'
epwName = '~/equipe-r/arquivos_climaticos/SP.epw'

### definicoes iniciais
list_epjson_names = runep_subprocess.gen_list_epjson_names(num_clusters)

runep_subprocess.gen_folders_clusters(num_clusters)
runep_subprocess.main(list_epjson_names, num_clusters)

os.chdir('..')

FOLDER_STDRD = 'cluster'
LEN_FOLDER_NAME = len(FOLDER_STDRD) +1
NUMBER_OF_DIGITS = 4  # ex. 0, 00, 000, 0000...
BASE_DIR = '/media/marcelo/OS/dissertacao/crack'
MONTH_MEANS = pd.read_csv('/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv')
MAX_THREADS = 10

folders = glob.glob(BASE_DIR+'/'+FOLDER_STDRD+'*')

print('Processing {} folders in \'{}\':'.format(len(folders), BASE_DIR))
for folder in folders:
    print('\t{}'.format(folder))

start_time = datetime.datetime.now()

num_folders = len(folders)
p = Pool(min(num_folders, MAX_THREADS))
p.map(temp_ach_multiprocess_cpeq.process_folder, folders)

end_time = datetime.datetime.now()

total_time = (end_time - start_time)

print("Total processing time: " + str(total_time))
