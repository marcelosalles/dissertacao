import glob
import subprocess
import os

def gen_folders_clusters(num_clusters):

    ### creates folders
    for cluster in range(num_clusters):

        folder_name = 'cluster%d' % (cluster)

        if os.path.isdir(folder_name):
            pass

        else:
            os.mkdir(folder_name)
            
def gen_list_epjson_names(num_clusters,extension = 'epJSON'):
    
    ### creates the list of files
    list_epjson_names = []
    
    for cluster in range(num_clusters):
        folder_name = 'cluster%d' % (cluster)
        os.chdir(folder_name)
        # list_epjson_names = list_epjson_names + glob.glob(folder_name+'/*.'+extension)
        list_epjson_names.append(sorted(glob.glob('*.'+extension)))   # list_epjson_names.append(glob.glob(folder_name+'/*.'+extension)) 
        os.chdir('..')
    return list_epjson_names

### execucao dos clusters
def simular(epjson_name, cluster,extension = 'epJSON',version_EnergyPlus = 'energyplus-8.9.0',epwName = '~/equipe-r/arquivos_climaticos/SP.epw'):

    folder_name = 'cluster%d' % (cluster)
    
    stringcluster = version_EnergyPlus + ' -w ' + epwName + ' -p ' + epjson_name.split('.'+extension)[0] + ' -r ' + epjson_name
    # print(stringcluster)

    os.chdir(folder_name)
    processing = subprocess.Popen(stringcluster, stdout = open(os.devnull, 'w'), stderr = subprocess.STDOUT, shell=True)
    os.chdir('..')

    return [processing, folder_name, epjson_name]


def main(list_epjson_names, num_clusters,extension = 'epJSON',remove_all_but = ['.epJSON', '.csv']):

    for _ in range(len(list_epjson_names[0])):
        list_execute = []

        for cluster in range(num_clusters):
            
            # print(len(list_epjson_names))

            if len(list_epjson_names[cluster]) > 0:

                epjson_name = list_epjson_names[cluster].pop(0)
                processing = simular(epjson_name, cluster)
                list_execute.append(processing)

        for i, line in enumerate(list_execute):
            list_execute[i][0].wait()
            print('Folder: ' + list_execute[i][1] + ' | ' + extension + ': ' + list_execute[i][2])

            internal_list = glob.glob(list_execute[i][1] + '/' + list_execute[i][2][:-(len(extension)+1)]+"*")
            
            for filename in internal_list:
                try:
                    if filename.split(list_execute[i][2][:-(len(extension)+1)]+'out')[1] not in remove_all_but:
                        os.remove(filename)
                except:
                    pass

    # if len(list_epjson_names[cluster]) > 0:
        # main(list_epjson_names, num_clusters)

if __name__ == '__main__':

    ### Mudar caso necessario
    extension = 'epJSON'
    version_EnergyPlus = 'energyplus-8.9.0'
    remove_all_but = ['.'+extension, '.csv']  # 'Table.csv'
    epwName = '~/equipe-r/arquivos_climaticos/SP.epw'

    ### definicoes iniciais
    num_clusters = int(os.cpu_count()/2)
    list_epjson_names = gen_list_epjson_names(num_clusters)  # glob.glob('*.'+extension)
    print(list_epjson_names)
    raiz = os.getcwd()

    gen_folders_clusters(num_clusters)
    main(list_epjson_names, num_clusters)
