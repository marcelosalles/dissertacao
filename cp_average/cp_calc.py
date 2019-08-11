import math
import pandas as pd

def cp_calc(ratio=1, bldg_type = 'lowrise', azimuth=0):
    
    # print(ratio, bldg_type, azimuth, room_type, cp_eq, zone_x, zone_y, wwr, zn, corner_window)
    
    surfaces = ['side_0_coef','side_1_coef','side_2_coef','side_3_coef']
      
    WindPressureCoefficientValues = {}
        
    for FacadeNum in range(4):
        WindPressureCoefficientValues[surfaces[FacadeNum]] = { }
        
        FacadeAng = (azimuth + FacadeNum * 90)%360
        if FacadeNum == 0 or FacadeNum == 2:
            SideRatio = 1.0 / ratio
        else:
            SideRatio = ratio
        
        SideRatioFac = math.log(SideRatio)
        
        for WindDirNum in range(12):
            WindAng = WindDirNum * 30.0
            IncAng = abs(WindAng - FacadeAng)
            
            if IncAng > 180.0:
                IncAng = 360.0 - IncAng
            
            IAng = int(IncAng / 30.0)
            DelAng = IncAng%30.0
            WtAng = 1.0 - DelAng / 30.0
            
            if bldg_type == 'lowrise':
                IncRad = IncAng * math.pi/180
                cos_IncRad_over_2 = math.cos(IncRad / 2.0)
                cp = 0.6 * math.log(1.248 - 0.703 * math.sin(IncRad / 2.0) - 1.175 * math.sin(IncRad)**2 +
                    0.131 * math.sin(2.0 * IncRad * SideRatioFac)**3 + 0.769 * cos_IncRad_over_2 +
                    0.07 * (SideRatioFac * math.sin(IncRad / 2.0))**2 + 0.717 * cos_IncRad_over_2**2)
            
            else:
                
                CPHighRiseWall = [
                    [0.60, 0.54, 0.23,  -0.25, -0.61, -0.55, -0.51, -0.55, -0.61, -0.25, 0.23,  0.54],
                    [0.60, 0.48, 0.04,  -0.56, -0.56, -0.42, -0.37, -0.42, -0.56, -0.56, 0.04,  0.48],
                    [0.60, 0.44, -0.26, -0.70, -0.53, -0.32, -0.22, -0.32, -0.53, -0.70, -0.26, 0.44]
                ]
                
                SR = min(max(SideRatio, 0.25), 4.0)
                if (SR >= 0.25 and SR < 1.0):
                    ISR = 0
                    WtSR = (1.0 - SR) / 0.75
                else:
                    ISR = 1
                    WtSR = (4.0 - SR) / 3.0
                    
                cp = WtSR * (WtAng * CPHighRiseWall[ISR][IAng] + (1.0 - WtAng) * CPHighRiseWall[ISR][IAng + 1]) + (1.0 - WtSR) * (WtAng * CPHighRiseWall[ISR + 1][IAng] + (1.0 - WtAng) * CPHighRiseWall[ISR + 1][IAng + 1])
                
            WindPressureCoefficientValues[surfaces[FacadeNum]]["angle_"+str(WindDirNum*30)] = cp
            
    return(WindPressureCoefficientValues)
    
lowrise_ratio = [1,2/3,2/5]
highrise_ratio = [1/1,2/1,3/1]

angles = [0,30,60,90,120,150,180,210,240,270,300,330]

bldg_type = []  # pd.Series(['lowrise' for l in range(len(lowrise_ratio)*4*len(angles))]+['highrise' for h in range(len(highrise_ratio)*4*len(angles))])

ratios = []
facade = []
angle = []
cp = []

for ratio in lowrise_ratio:
    
    cps = cp_calc(ratio=ratio,bldg_type = 'lowrise')
    
    angle_i = 0    
    for a in cps['side_0_coef']:
        
        ratios.append(ratio)
        bldg_type.append('lowrise')
        facade.append(1)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_0_coef'][a])
        
    angle_i = 0    
    for a in cps['side_1_coef']:
        
        ratios.append(ratio)
        bldg_type.append('lowrise')
        facade.append(2)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_1_coef'][a])
        
    angle_i = 0    
    for a in cps['side_2_coef']:
        
        ratios.append(ratio)
        bldg_type.append('lowrise')
        facade.append(3)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_2_coef'][a])
        
    angle_i = 0    
    for a in cps['side_3_coef']:
        
        ratios.append(ratio)
        bldg_type.append('lowrise')
        facade.append(4)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_3_coef'][a])

for ratio in highrise_ratio:
    
    cps = cp_calc(ratio=ratio,bldg_type = 'lowrise')
        
    angle_i = 0    
    for a in cps['side_0_coef']:
        
        ratios.append(ratio)
        bldg_type.append('highrise')
        facade.append(1)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_0_coef'][a])
        
    angle_i = 0    
    for a in cps['side_1_coef']:
        
        ratios.append(ratio)
        bldg_type.append('highrise')
        facade.append(2)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_1_coef'][a])
        
    angle_i = 0    
    for a in cps['side_2_coef']:
        
        ratios.append(ratio)
        bldg_type.append('highrise')
        facade.append(3)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_2_coef'][a])
        
    angle_i = 0    
    for a in cps['side_3_coef']:
        
        ratios.append(ratio)
        bldg_type.append('highrise')
        facade.append(4)
        angle.append(angle_i*30)
        angle_i += 1
        cp.append(cps['side_3_coef'][a])

df = pd.DataFrame({'bldg_type':bldg_type,'ratio':ratios,'facade':facade,'angle':angle,'Cp':cp})

df.to_csv('df_cp_average.csv',index=False)

'''
setwd('/media/marcelo/OS/Cps/')

df <- read.csv('df_cp_average.csv')

tpu_data <- dir(pattern = '.mat')

for (file in tpu_data){
  print(file)
  opened_file = read.csv(file)
  df_file = open
}

'side_0_coef': {'airflownetwork_multizone_windpressurecoefficientarray_name': 'ventos', 'idf_max_extensible_fields': 0, 'idf_max_fields': 14, 
'wind_pressure_coefficient_value_1': 0.6034594429810546, 0
'wind_pressure_coefficient_value_2': 0.46871331767731117, 30
'wind_pressure_coefficient_value_3': 0.11880548415819636, 60
'wind_pressure_coefficient_value_4': -0.4426745718194904, 90
'wind_pressure_coefficient_value_5': -0.6805110858003989, 120 
'wind_pressure_coefficient_value_6': -0.38974708034386035, 150
'wind_pressure_coefficient_value_7': -0.3641816905913357, 180
'wind_pressure_coefficient_value_8': -0.38974708034386035, 210
'wind_pressure_coefficient_value_9': -0.6805110858003989,  240
'wind_pressure_coefficient_value_10': -0.4426745718194904, 270
'wind_pressure_coefficient_value_11': 0.11880548415819636,  300
'wind_pressure_coefficient_value_12': 0.46871331767731117} 330

'side_1_coef': {'airflownetwork_multizone_windpressurecoefficientarray_name': 'ventos', 'idf_max_extensible_fields': 0, 'idf_max_fields': 14, 
'wind_pressure_coefficient_value_1': -0.4426745718194904, 
'wind_pressure_coefficient_value_2': 0.11880548415819636, 
'wind_pressure_coefficient_value_3': 0.46871331767731117, 
'wind_pressure_coefficient_value_4': 0.6034594429810546, 
'wind_pressure_coefficient_value_5': 0.46871331767731117, 
'wind_pressure_coefficient_value_6': 0.11880548415819636, 
'wind_pressure_coefficient_value_7': -0.4426745718194904, 
'wind_pressure_coefficient_value_8': -0.6805110858003989, 
'wind_pressure_coefficient_value_9': -0.38974708034386035, 
'wind_pressure_coefficient_value_10': -0.3641816905913357, 
'wind_pressure_coefficient_value_11': -0.38974708034386035, 
'wind_pressure_coefficient_value_12': -0.6805110858003989}, 

'side_2_coef': {'airflownetwork_multizone_windpressurecoefficientarray_name': 'ventos', 'idf_max_extensible_fields': 0, 'idf_max_fields': 14, 
'wind_pressure_coefficient_value_1': -0.3641816905913357, 
'wind_pressure_coefficient_value_2': -0.38974708034386035, 
'wind_pressure_coefficient_value_3': -0.6805110858003989, 
'wind_pressure_coefficient_value_4': -0.4426745718194904, 
'wind_pressure_coefficient_value_5': 0.11880548415819636, 
'wind_pressure_coefficient_value_6': 0.46871331767731117, 
'wind_pressure_coefficient_value_7': 0.6034594429810546, 
'wind_pressure_coefficient_value_8': 0.46871331767731117, 
'wind_pressure_coefficient_value_9': 0.11880548415819636, 
'wind_pressure_coefficient_value_10': -0.4426745718194904, 
'wind_pressure_coefficient_value_11': -0.6805110858003989, 
'wind_pressure_coefficient_value_12': -0.38974708034386035},

'side_3_coef': {'airflownetwork_multizone_windpressurecoefficientarray_name': 'ventos', 'idf_max_extensible_fields': 0, 'idf_max_fields': 14, 
'wind_pressure_coefficient_value_1': -0.4426745718194904, 
'wind_pressure_coefficient_value_2': -0.6805110858003989,
'wind_pressure_coefficient_value_3': -0.38974708034386035, 
'wind_pressure_coefficient_value_4': -0.3641816905913357, 
'wind_pressure_coefficient_value_5': -0.38974708034386035, 
'wind_pressure_coefficient_value_6': -0.6805110858003989, 
'wind_pressure_coefficient_value_7': -0.4426745718194904, 
'wind_pressure_coefficient_value_8': 0.11880548415819636, 
'wind_pressure_coefficient_value_9': 0.46871331767731117, 
'wind_pressure_coefficient_value_10': 0.6034594429810546, 
'wind_pressure_coefficient_value_11': 0.46871331767731117, 
'wind_pressure_coefficient_value_12': 0.11880548415819636}}
'''
