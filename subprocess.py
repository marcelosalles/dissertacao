import glob
import subprocess
import os

def gen_folders_clusters(num_clusters):

	### criacao das Folders
	for cluster in range(num_clusters):

		folder_name = 'cluster%d' % (cluster)

		if os.path.isdir(folder_name):
			pass

		else:
			os.mkdir(folder_name)

### execucao dos clusters
def simular(epjson_name, cluster):

	folder_name = 'cluster%d' % (cluster)
    
	stringcluster = versaoEnergyPlus + ' -w ' + epwName + ' -p ' + epjson_name.split('.'+extension)[0] + ' -r ' + epjson_name 

	os.chdir(folder_name)
	processing = subprocess.Popen(stringcluster, stdout = open(os.devnull, 'w'), stderr = subprocess.STDOUT, shell=True)
	os.chdir('..')

	return [processing, folder_name, epjson_name]


def main(list_epjson_names, num_clusters):

	list_execute = []

	for cluster in range(num_clusters):

		if len(list_epjson_names) > 0:

			epjson_name = list_epjson_names.pop(0)
			processing = simular(epjson_name, cluster)
			list_execute.append(processing)

	for i, line in enumerate(list_execute):
		list_execute[i][0].wait()
		print('Folder: ' + list_execute[i][1] + ' | ' + extension + list_execute[i][2])

		internal_list = glob.glob(list_execute[i][2][:-len(extension)]+"*")
		for filename in internal_list:
			if filename.split(list_execute[i][2][:-(len(extension)+1)]+'out')[1] not in remove_all_but:
				os.remove(filename)

	if len(list_epjson_names) > 0:
		main(list_epjson_names, num_clusters)

if __name__ == '__main__':

	### Mudar caso necessario
    extension = 'epJSON'
	versaoEnergyPlus = 'energyplus-8.9.0'
	remove_all_but = ['.'+extension, '.csv', 'Table.csv']
	epwName = '~/equipe-r/arquivos_climaticos/SP.epw'

	### definicoes iniciais
	list_epjson_names = glob.glob('*.'+extension)
	num_clusters = int(os.cpu_count()/2)
	raiz = os.getcwd()

	gen_folders_clusters(num_clusters)
	main(list_epjson_names, num_clusters)
