# Return EHF from multiple simulation results of Operative Temperature

## BIBLIOTECAS
import glob  # lista os arquivos na pasta
from multiprocessing import Pool  # possibilita processos multithread
import os  # possibilita comandos no sistema operacional
import pandas as pd  # facilita trabalhar com dataframes
from dict_update import update  # atualiza dicionários

def set_delta_T(n):
    # Destermina o aumento na faixa de tolerancia de temperatura,
    # quando considerado o movimento do ar, a partir do valor amostrado.
    # Inputs:
    # n = numero amostrado (entre 0 e 1)
    # Outputs:
    # delta_T = margem de temperatura adotada

    if n < .25:
        delta_T = 0
    elif n < .5:
        delta_T = 1.2
    elif n < .75:
        delta_T = 1.8
    else:
        delta_T = 2.2
    
    return delta_T

def process_outputs(line, month_means, ach=True):
    # Le o output do energyplus para o caso especificado e calcula a
    # temperatura operativa média, temperatura operativa máxima, a
    # média das trocas de ar por hora (ACH), e o EHF.
    # Inputs:
    # line = a linha do dataframe que especifica o caso avaliado.
    # month_means = um dataframe com o mesmo numero de linhas que o
    ## output do EnergyPlus, com o valor da temperatura de conforto,
    ## de acordo com o modelo adaptativo da ASHRAE 55, para cada timestep.
    # ach = define se o ACH vai ser considerado no dataframe, ou nao.
    # Output:
    # df_temp = dicionario com todas as informacoes desejadas
    
    # dicioniario (dataframe) criado para adicinar as informacoes
    df_temp = {
        'folder': [],
        'file': [],
        'zone': [],
        'temp': [],
        'temp_max': [],
        'ach': [],
        'ehf': []
    }
        
    # printa o nome do arquivo para podermos acompanhar o processo
    print(line['file'],' ',line['folder'])  # , end='\r')
    
    # define o nome do output do energyplus a partir do nome do idf
    csv_file = line['file'].split('.')[0]+'out.csv'
    
    # le o output como um dataframe, utilizando o pandas
    df = pd.read_csv(line['folder']+'/'+csv_file)
    
    # a partir do parametro que define a velocidade do ar, calcula delta_T
    delta_T = set_delta_T(line['v_ar'])
    
    # confere se eh "single zone", ou "whole building"    
    if line['file'][0] == 'w':  # se a primeira letra do nome do arquivo eh "w", é "whole building"
        n_zones = 6  # os modelos "whole building" possuem 6 zonas
        
        for zn in range(n_zones):  # repete o processo para cada zona. esta melhor explicado abaixo
            
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
    
    else: # calculo dos outputs para o caso "single zone"
        
        df_temp['file'].append(line['file'].split('.')[0])  # nome do arquivo sem a extensao
        df_temp['folder'].append(line['folder'])  # nome da pasta onde está o arquivo
        df_temp['zone'].append(line['file'].split('.')[0][-1])  # o numero da zona equivalente eh o ultimo caractere do nome do arquivo

        df_temp['temp'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())  # add no df_temp a temp op media, com ocupacao
        df_temp['temp_max'].append((df['OFFICE:Zone Operative Temperature [C](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).max())  # add no df_temp a temp op maxima, com ocupacao
        if ach:
            df_temp['ach'].append((df['OFFICE:AFN Zone Infiltration Air Change Rate [ach](Hourly)'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0]).mean())  # add no df_temp o ach medio, com ocupacao
        else:
            df_temp['ach'].append(0)  # se ach = False, valor é sempre 0
            
        df['E_hot'] = -1  # cria um vetor para sinalizar se a temperatura passa o limite ou não (o valor -1 eh arbitrario, pois vai ser substituido posteriormente)
        df['sup_lim'] = month_means['mean_temp'] + 3.5 + delta_T  # cria um vetor com o limite superior de temp op. 3.5 é a marge para 80% de aceitabilidade
        df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] > df['sup_lim'], 'E_hot'] = 1  # adiciona o valor 1 no vetor "E_hot", se a temp op ultrapassa o limite
        df.loc[df['OFFICE:Zone Operative Temperature [C](Hourly)'] <= df['sup_lim'], 'E_hot'] = 0  # adiciona o valor 0 no vetor "E_hot", se a temp op nao ultrapassa o limite
            
        df_temp['ehf'].append(df['E_hot'][df['SCH_OCUPACAO:Schedule Value [](Hourly)'] > 0].mean())  # EHF eh igual a media do vetor "E_hot"
    
    return(df_temp)

def main(df_base, month_means, output_name, ach=True):
    # Manda calcular os outputs desejados para cada caso do dataframe,
    # utilizando processos multiplos (multithread)
    # Inputs:
    # df_base = dataframe com as informações de todos os casos.
    # month_means = utilizado para a funcao process_outputs.
    # output_name = nome com que o dataframe gerada sera salvo.
    # ach = utilizado para a funcao process_outputs.
    
    # dicioniario (dataframe) criado para adicinar as informacoes
    df_final = {
        'folder': [],
        'file': [],
        'zone': [],
        'temp': [],
        'temp_max': [],
        'ach': [],
        'ehf': []
    }
    
    # Month means ja foi calculado e eh lido como um dataframe, utilizando pandas (neste caso o clima eh sempre o mesmo)
    MONTH_MEANS = pd.read_csv(month_means)

    # o numero de clusters eh defido a partir do numero de pastas (nao precisa ser assim)
    num_cluster = len(df_base['folder'].unique())
    
    p = Pool(num_cluster)  # abre os multi processos

    # manda rodar a funcao process_outputs para os multiprocessos
    result_map = p.starmap(process_outputs, zip(
        # [df_base.query('folder == "cluster'+str(i)+'"') for i in range(num_cluster)],
        [df_base.iloc[i] for i in range(len(df_base))],
        [MONTH_MEANS for _ in range(len(df_base))],
        [output_name for _ in range(len(df_base))],
        [ach for _ in range(len(df_base))]
    ))
    p.close()
    p.join()

    # passa os resultados dos multi processos para o df_final
    for df_temp in result_map:
        for key in df_final.keys():
            for i in range(len(df_temp[key])):
                df_final[key].append(df_temp[key][i])
    
    # salva o df_final como csv
    df_output = pd.DataFrame(df_final)
    df_output.to_csv(output_name+'.csv', index=False)
    print('\tDone processing!')

'''
Teste da funcao sem depender de outros codigos:

df_base = pd.read_csv('test.csv')
os.chdir('test')
main(df_base, '/media/marcelo/OS/LabEEE_1-2/idf-creator/month_means_8760.csv', 'teste')
'''