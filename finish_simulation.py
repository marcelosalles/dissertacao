import os

FOLDER = 'cpeq'
WEATHER_FILE = '/home/marcelo/equipe-r/arquivos_climaticos/SP.epw'
WHOLE_STRD = 'whole'
SZ_STRD = 'single'

for i in range(10):

    for j in range(100):
        
        exists = os.path.isfile(FOLDER+'/cluster'+str(i)+'/'+WHOLE_STRD+'_{:04.0f}'.format(i*100+j)+'out.csv')
        if not exists:
            print(''+WHOLE_STRD+'_{:04.0f}'.format(i*100+j),'\n')
            os.system('energyplus-8.9.0 -w '+WEATHER_FILE+' -p '+FOLDER+'/cluster'+str(i)+'/'+WHOLE_STRD+'_{:04.0f}'.format(i*100+j)+' -r '+FOLDER+'/cluster'+str(i)+'/'+WHOLE_STRD+'_{:04.0f}'.format(i*100+j)+'.epJSON')
        
        for k in range(6):
        
            exists = os.path.isfile(FOLDER+'/cluster'+str(i)+'/'+SZ_STRD+'_{:04.0f}'.format(i*100+j)+'_'+str(k)+'out.csv')
            if not exists:
                print(''+WHOLE_STRD+'_{:04.0f}'.format(i*100+j)+'_'+str(k),'\n')
                os.system('energyplus-8.9.0 -w '+WEATHER_FILE+' -p '+FOLDER+'/cluster'+str(i)+'/'+SZ_STRD+'_{:04.0f}'.format(i*100+j)+'_'+str(k)+' -r '+FOLDER+'/cluster'+str(i)+'/'+SZ_STRD+'_{:04.0f}'.format(i*100+j)+'_'+str(k)+'.epJSON')
        
            # exists = os.path.isfile(FOLDER+'/cluster'+str(i)+'/adiabatic_{:04.0f}'.format(i*100+j)+'_'+str(k)+'out.csv')
            # if not exists:
                # print('adiabatic_{:04.0f}'.format(i*100+j)+'_'+str(k),'\n')
                # os.system('energyplus-8.9.0 -w '+WEATHER_FILE+' -p '+FOLDER+'/cluster'+str(i)+'/adiabatic_{:04.0f}'.format(i*100+j)+'_'+str(k)+' -r '+FOLDER+'/cluster'+str(i)+'/adiabatic_{:04.0f}'.format(i*100+j)+'_'+str(k)+'.epJSON')
