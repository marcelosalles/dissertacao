from singlezone_diss import main
import pandas as pd

N_CLUSTERS = 10
INPUT_FILE = 'sample_04_22.csv'
FOLDER = '04-22'  # 'lhs'
NAME_STDRD = 'lhs'

###load samples
sample = pd.read_csv(INPUT_FILE)
# sample = sample[:10]  # para teste

samples_x_cluster = len(sample)/N_CLUSTERS

# min's and max's
MIN_AREA = 20
MAX_AREA = 100

MIN_RATIO = .5
MAX_RATIO = 2

MIN_ZONE_HEIGHT = 2.4
MAX_ZONE_HEIGHT = 3.2

MIN_ABS = .3
MAX_ABS = .9

MIN_SHADING = 0
MAX_SHADING = 1

MIN_AZIMUTH = 0
MAX_AZIMUTH = 359.9

MIN_WALL_U = 0.5
MAX_WALL_U = 4.4

MIN_WALL_CT = 20
MAX_WALL_CT = 400

MIN_WWR = .1
MAX_WWR = .6

MIN_OPENFAC = 0.1
MAX_OPENFAC = 1

MIN_PEOPLE = .05
MAX_PEOPLE = .5

MIN_FS = .2
MAX_FS = .87

MIN_FLOOR_HEIGHT = 0
MAX_FLOOR_HEIGHT = 30

MIN_BLDG_RATIO = .25
MAX_BLDG_RATIO = 4

BOUNDS = {
    'area':{
        'min': MIN_AREA,
        'max': MAX_AREA
    },
    'ratio':{
        'min': MIN_RATIO,
        'max': MAX_RATIO
    },
    'zone_height':{
        'min': MIN_ZONE_HEIGHT,
        'max': MAX_ZONE_HEIGHT
    },
    'abs':{
        'min': MIN_ABS,
        'max': MAX_ABS
    },
    'shading':{
        'min': MIN_SHADING,
        'max': MAX_SHADING
    },
    'azimuth':{
        'min': MIN_AZIMUTH,
        'max': MAX_AZIMUTH
    },
    'wall_u':{
        'min': MIN_WALL_U,
        'max': MAX_WALL_U
    },
    'wall_ct':{
        'min': MIN_WALL_CT,
        'max': MAX_WALL_CT
    },
    'wwr':{
        'min': MIN_WWR,
        'max': MAX_WWR
    },
    'open_fac':{
        'min': MIN_OPENFAC,
        'max': MAX_OPENFAC
    },
    'people':{
        'min': MIN_PEOPLE,
        'max': MAX_PEOPLE
    },
    'glass':{
        'min': MIN_FS,
        'max': MAX_FS
    },
    'floor_height':{
        'min': MIN_FLOOR_HEIGHT,
        'max': MAX_FLOOR_HEIGHT
    },
    'bldg_ratio':{
        'min': MIN_BLDG_RATIO,
        'max': MAX_BLDG_RATIO
    }
}

# means and sd
for parameter in BOUNDS:
    mean = (BOUNDS[parameter]['max']+BOUNDS[parameter]['min'])*.5
    sd = BOUNDS[parameter]['max']-mean
    BOUNDS[parameter]['mean'] = mean
    BOUNDS[parameter]['sd'] = sd

# prepare inputs
for col in sample:
    if col in list(BOUNDS):
        sample[col] = BOUNDS[col]['mean']+BOUNDS[col]['sd']*sample[col]

# start iteration
for line in range(len(sample)):

    # prepare inputs
    area = sample['area'][line]
    ratio = sample['ratio'][line]
    zone_height = sample['zone_height'][line]
    absorptance = sample['abs'][line]
    shading = 0  # sample['shading'][line]
    azimuth = sample['azimuth'][line]
    wall_u = sample['wall_u'][line]
    wall_ct = 155  # sample['wall_ct'][line]
    wwr = sample['wwr'][line]
    open_fac = sample['open_fac'][line]
    people = sample['people'][line]
    glass = .87  # sample['glass'][line]
    floor_height = 15  # sample['floor_height'][line]
    bldg_ratio = 1  # sample['bldg_ratio'][line]
    
    if sample['room_type'][line] < -.6:
        # room_type = '1_window'
        zn = 1
        corner_window = True
    elif sample['room_type'][line] < -.2:
        # room_type = '3_window'
        zn = 0
        corner_window = True
    elif sample['room_type'][line] < .2:
        # room_type = '1_wall'
        zn = 1
        corner_window = False
    elif sample['room_type'][line] < .6:
        # room_type = '3_wall'
        zn = 0
        corner_window = False
    else:
        # room_type = '0_window'
        zn = 2
        corner_window = True
        
    if sample['ground'][line] < 0:
        ground = 0
    else:
        ground = 1
        
    if sample['roof'][line] < 0:
        roof = 0
    else:
        roof = 1
    
    cluster_n = int(line//samples_x_cluster)
    
    caso = '{:06.0f}'.format(line)
    output = (FOLDER+'/cluster'+'{:01.0f}'.format(cluster_n)+'/'+NAME_STDRD+'_{}.epJSON'.format(caso))

    main(zone_area=area, zone_ratio=ratio, zone_height=zone_height,
    absorptance=absorptance, shading=shading, azimuth=azimuth,
    bldg_ratio=bldg_ratio, wall_u=wall_u, wall_ct=wall_ct, zn=zn,
    floor_height=floor_height, corner_window=corner_window, ground=ground,
    roof=roof, people=people, glass_fs=glass, wwr=wwr, open_fac=open_fac,
    input_file="seed_single_U-conc-eps.json", output=output)
