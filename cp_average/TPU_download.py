import urllib.request as ur

hr_bldg_90 = ['T312','T313','T314','T315',
    'T212','T213','T214','T215']

hr_bldg_45 = ['T111','T112','T113','T114','T115']

lr_bldg = ['g080800','g120800','g200800',
    'g080600','g120600','g200600',
    'g080400','g120400','g200400',
    'g080200','g120200','g200200']

# for bldg in hr_bldg_90:
    
    # for angle in range(21):
        
        # file_name = bldg+'_4_{:03d}'.format(angle*5)+'_1.mat'
        # ur.urlretrieve('http://www.wind.arch.t-kougei.ac.jp/info_center/windpressure/highrise/Test_Data/'+file_name, file_name)
        # print(file_name)

# for bldg in hr_bldg_45:
    
    # for angle in range(11):
        
        # file_name = bldg+'_4_{:03d}'.format(angle*5)+'_1.mat'
        # ur.urlretrieve('http://www.wind.arch.t-kougei.ac.jp/info_center/windpressure/highrise/Test_Data/'+file_name, file_name)
        # print(file_name)

for bldg in lr_bldg:
    
    for angle in range(7):
        
        file_name = 'Cp_ts_'+bldg+'{:02d}'.format(angle*15)+'.mat'
        ur.urlretrieve('http://www.wind.arch.t-kougei.ac.jp/info_center/windpressure/lowrise/'+file_name, file_name)
        print(file_name)
