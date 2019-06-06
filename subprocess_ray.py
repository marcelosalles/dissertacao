import glob
import subprocess
import os

def criarPastasProcessos(numeroProcessos):

	### criacao das pastas
	for processo in range(numeroProcessos):

		nomePasta = 'processo%d' % (processo)

		if os.path.isdir(nomePasta):
			pass

		else:
			os.mkdir(nomePasta)

### execucao dos processos
def simular(idfName, processo):

	nomePasta = 'processo%d' % (processo)
	caminhoCompletoParteIdf = os.path.join(raiz, idfName[:-4])
	stringProcesso = 'CALL C:\\EnergyPlusV%s\\RunEPlus.bat ' % (versaoEnergyPlus) + '"' + caminhoCompletoParteIdf + '" ' + epwName + '\nEXIT'

	os.chdir(nomePasta)
	processando = subprocess.Popen(stringProcesso, stdout = open(os.devnull, 'w'), stderr = subprocess.STDOUT, shell=True)
	os.chdir('..')

	return [processando, nomePasta, idfName]


def main(listaIdfNames, numeroProcessos):

	listaExecucao = []

	for processo in range(numeroProcessos):

		if len(listaIdfNames) > 0:

			idfName = listaIdfNames.pop(0)
			processando = simular(idfName, processo)
			listaExecucao.append(processando)

	for i, line in enumerate(listaExecucao):
		listaExecucao[i][0].wait()
		print('Pasta: ' + listaExecucao[i][1] + ' | ' + 'IDF: ' + listaExecucao[i][2])

		listaInterna = glob.glob(listaExecucao[i][2][:-3]+"*")
		for arquivo in listaInterna:
			if arquivo.split(listaExecucao[i][2][:-4])[1] not in removerTodosMenos:
				os.remove(arquivo)

	if len(listaIdfNames) > 0:
		main(listaIdfNames, numeroProcessos)

if __name__ == '__main__':

	### Mudar caso necessario
	versaoEnergyPlus = '9-1-0'
	removerTodosMenos = ['.idf', '.csv', 'Table.csv']
	epwName = 'climas/unique'

	### definicoes iniciais
	listaIdfNames = glob.glob('*.idf')
	numeroProcessos = 2 #int(os.cpu_count()/2)
	raiz = os.getcwd()

	criarPastasProcessos(numeroProcessos)
	main(listaIdfNames, numeroProcessos)
