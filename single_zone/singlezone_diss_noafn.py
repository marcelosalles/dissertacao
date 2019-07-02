# The names given to the surfaces go from 0 to 3, being 0 up, 1 right,
# 2 down, 3 left. 

import collections
import json

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
    
def main(zone_area=10, zone_ratio=1, zone_height=3, absorptance=.5,
    shading=1, azimuth=0, bldg_ratio=1, wall_u=2.5, wall_ct=100,
    zn=0, floor_height=0, corner_window=True, ground=0, roof=0, 
    people=.1, glass_fs=.87, wwr=.6, outdoors=False,
    input_file='seed.json' , output='output.epJSON'):
    
    print(output)

    # Making sure numbers are not srings ----------

    zone_area = float(zone_area)
    zone_ratio = float(zone_ratio)
    zone_height = float(zone_height)
    absorptance = float(absorptance)
    shading = float(shading)
    azimuth = float(azimuth)
    bldg_ratio = float(bldg_ratio)
    wall_u = float(wall_u)
    wall_ct = float(wall_ct)
    floor_height = float(floor_height)
    glass_fs = float(glass_fs)
    wwr = float(wwr)
    
    if zn == 0:
        if corner_window:
            room_type = '3_window'
        else:
            room_type = '3_wall'
    elif zn == 1:
        if corner_window:
            room_type = '1_window'
        else:
            room_type = '1_wall'
    elif zn == 2:
        room_type = '0_window'
    elif zn == 3:
        room_type = '0_window'
    elif zn == 4:
        if corner_window:
            room_type = '1_window'
        else:
            room_type = '1_wall'
    elif zn == 5:
        if corner_window:
            room_type = '3_window'
        else:
            room_type = '3_wall'
        
    if outdoors:
        corrwall = "Outdoors"
    else:
        corrwall = "Adiabatic"
        
    # editing thermal load

    # electric = float(thermal_loads)
    people = float(people)
    lights = 10.50  # DPI nivel A RTQ-R - Escritorio Planta livre

    # Defining U

    c_concrete = 1.75  # condutivity
    e_concrete = (wall_ct*1000)/(1000*2200)  # specific heat and density
    R_concrete = e_concrete/c_concrete
    R_eps = (1-(.17+R_concrete)*wall_u)/wall_u
    eps = True
    if R_eps < 0.001:
        eps = False
        c_concrete = (wall_u*e_concrete)/(1-.17*wall_u)
        print('conductivity concrete: ', c_concrete)
        print('wall_u: ', wall_u, '\n', 'wall_ct: ', wall_ct)
        
    # Defining dependent variables ----------

    zone_x = (zone_area/zone_ratio)**(1/2)
    zone_y = (zone_area /zone_x)
    window_x1 = zone_x*.001
    window_x2 = zone_x*.999
    window_y1 = zone_y*.001
    window_y2 = zone_y*.999

    window_z1 = zone_height*(1-wwr)*.5
    window_z2 = window_z1+(zone_height*wwr)

    door_width = .9
    dist_door_wall = .1
    door_height = 2.1

    # START BUILDING OBJECTS
    model = dict()

    ##### Building
    model["Building"] = {
        output[:-7]: {
            "loads_convergence_tolerance_value": 0.04,
            "maximum_number_of_warmup_days": 25,
            "north_axis": azimuth,
            "solar_distribution": "FullInteriorAndExterior",
            "temperature_convergence_tolerance_value": 0.4,
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 8,
            "terrain": "City"
        }
    }

    ##### ZONES
    model["Zone"] = {
        "office": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 7,
            "direction_of_relative_north": 0.0,
            "multiplier": 1,
            "x_origin": 0,
            "y_origin": 0,
            "z_origin": floor_height
        }
    }

    ##### Building Surface
    model["BuildingSurface:Detailed"] = {

        # Ceiling
        "ceiling_office": {
            "vertices": [
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": zone_height
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": zone_height
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": zone_height
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": zone_height
                }
            ],
            "zone_name": "office"
        },

        # Floor
        "floor_office": {
            "surface_type": "Floor",
            "vertices": [
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": 0.0
                }
            ],
            "zone_name": "office"
        },

        # Walls: 0 = up, 1 = right, 2 = down, 3 = left
        "wall-0_office": {
            "surface_type": "Wall",
            "construction_name": "Exterior Wall",
            "outside_boundary_condition": "Outdoors",
            "sun_exposure": "SunExposed",
            "wind_exposure": "WindExposed",
            "vertices": [
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": zone_height
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": zone_height
                }
            ],
            "zone_name": "office"
        },
        "wall-1_office": {
            "surface_type": "Wall",
            "vertices": [
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": zone_height
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": zone_height
                }
            ],
            "zone_name": "office"
        },
        "wall-2_office": {
            "surface_type": "Wall",
            "construction_name": "Interior Wall",
            "outside_boundary_condition": corrwall,
            "outside_boundary_condition_object": "",
            "sun_exposure": "NoSun",
            "wind_exposure": "NoWind",
            "vertices": [
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": zone_height
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": zone_height
                }
            ],
            "zone_name": "office"
        },
        "wall-3_office": {
            "surface_type": "Wall",
            "vertices": [
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": zone_height
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": zone_y,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": 0.0
                },
                {
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": zone_height
                }
            ],
            "zone_name": "office"
        }
    }

    # Top Condition
    if roof == 0:
        ceiling_bound = {
            "construction_name": "Interior Ceiling",
            "outside_boundary_condition": "Adiabatic",
            "sun_exposure": "NoSun",
            "surface_type": "Ceiling",
            "wind_exposure": "NoWind"
        }

    else:
        ceiling_bound = {
            "construction_name": "Exterior Roof",
            "outside_boundary_condition": "Outdoors",
            "sun_exposure": "SunExposed",
            "surface_type": "Roof",
            "wind_exposure": "WindExposed"
        }

    model["BuildingSurface:Detailed"]["ceiling_office"].update(ceiling_bound)

    # Bottom condition
    if ground == 0:
        ground_bound = {
            "construction_name": "Interior Floor",
            "outside_boundary_condition": "Adiabatic",
            "sun_exposure": "NoSun",
            "wind_exposure": "NoWind"
        }

    else:
        ground_bound = {
            "construction_name": "Exterior Floor",
            "outside_boundary_condition": "Ground",
            "sun_exposure": "NoSun",
            "wind_exposure": "NoWind"
        }

    model["BuildingSurface:Detailed"]["floor_office"].update(ground_bound)

    # Wall exposition condition
    exposed_wall = {
        "construction_name": "Exterior Wall",
        "outside_boundary_condition": "Outdoors",
        "sun_exposure": "SunExposed",
        "wind_exposure": "WindExposed"
    }
    interior_wall = {
        "construction_name": "Interior Wall",
        "outside_boundary_condition": "Adiabatic",
        "sun_exposure": "NoSun",
        "wind_exposure": "NoWind"
    }

    if room_type == '0_window':
        model["BuildingSurface:Detailed"]["wall-1_office"].update(interior_wall)
        model["BuildingSurface:Detailed"]["wall-3_office"].update(interior_wall)

    elif room_type == '1_window' or room_type == '1_wall':
        model["BuildingSurface:Detailed"]["wall-1_office"].update(exposed_wall)
        model["BuildingSurface:Detailed"]["wall-3_office"].update(interior_wall)

    elif room_type == '3_window' or room_type == '3_wall':
        model["BuildingSurface:Detailed"]["wall-1_office"].update(interior_wall)
        model["BuildingSurface:Detailed"]["wall-3_office"].update(exposed_wall)
    else:
        print('ROOM TYPE NON EXISTENT!!!')

    # Add some needed information

    needed_info = {
        "idf_max_extensible_fields": 12,
        "idf_max_fields": 22,
        "number_of_vertices": 4.0
    }

    for obj in model["BuildingSurface:Detailed"]:
        model["BuildingSurface:Detailed"][obj].update(needed_info)

    #### FENESTRATION

    model["FenestrationSurface:Detailed"] = {
        "window_0_office": {
            "building_surface_name": "wall-0_office",
            "construction_name": "glass_construction_office",
            "number_of_vertices": 4.0,
            "surface_type": "Window",
            "vertex_1_x_coordinate": window_x2,
            "vertex_1_y_coordinate": zone_y,
            "vertex_1_z_coordinate": window_z2,
            "vertex_2_x_coordinate": window_x2,
            "vertex_2_y_coordinate": zone_y,
            "vertex_2_z_coordinate": window_z1,
            "vertex_3_x_coordinate": window_x1,
            "vertex_3_y_coordinate": zone_y,
            "vertex_3_z_coordinate": window_z1,
            "vertex_4_x_coordinate": window_x1,
            "vertex_4_y_coordinate": zone_y,
            "vertex_4_z_coordinate": window_z2
        }
    }

    if room_type == '1_window':
        model["FenestrationSurface:Detailed"].update({
            "window_side_office": {
                "building_surface_name": "wall-1_office",
                "construction_name": "glass_construction_office",
                "number_of_vertices": 4.0,
                "surface_type": "Window",
                "vertex_1_x_coordinate": zone_x,
                "vertex_1_y_coordinate": window_y1,
                "vertex_1_z_coordinate": window_z2,
                "vertex_2_x_coordinate": zone_x,
                "vertex_2_y_coordinate": window_y1,
                "vertex_2_z_coordinate": window_z1,
                "vertex_3_x_coordinate": zone_x,
                "vertex_3_y_coordinate": window_y2,
                "vertex_3_z_coordinate": window_z1,
                "vertex_4_x_coordinate": zone_x,
                "vertex_4_y_coordinate": window_y2,
                "vertex_4_z_coordinate": window_z2
            }
        })

    elif room_type == '3_window':
        model["FenestrationSurface:Detailed"].update({
            "window_side_office": {
                "building_surface_name": "wall-3_office",
                "construction_name": "glass_construction_office",
                "number_of_vertices": 4.0,
                "surface_type": "Window",
                "vertex_1_x_coordinate": 0,
                "vertex_1_y_coordinate": window_y2,
                "vertex_1_z_coordinate": window_z2,
                "vertex_2_x_coordinate": 0,
                "vertex_2_y_coordinate": window_y2,
                "vertex_2_z_coordinate": window_z1,
                "vertex_3_x_coordinate": 0,
                "vertex_3_y_coordinate": window_y1,
                "vertex_3_z_coordinate": window_z1,
                "vertex_4_x_coordinate": 0,
                "vertex_4_y_coordinate": window_y1,
                "vertex_4_z_coordinate": window_z2
            }
        })
    
    for obj in model['FenestrationSurface:Detailed']:
        model['FenestrationSurface:Detailed'][obj].update({
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 22
        })
    
    #### SHADING vertex_x_coordinate
    
    
    if shading > 0.01:
		
        y_shading = zone_y
        z_shading = floor_height+window_z2
        
        model['Shading:Building:Detailed'] = {
            'shading_0': {
                "idf_max_extensible_fields": 12,
                "idf_max_fields": 15,
                'transmittance_schedule_name': '',
                'number_of_vertices': 4,
                "vertices": [
                    {
                    "vertex_x_coordinate": 0,
                    "vertex_y_coordinate": y_shading+shading,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": 0,
                    "vertex_y_coordinate": y_shading,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": y_shading,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": y_shading+shading,
                    "vertex_z_coordinate": z_shading
                    }
                ]
            }
        }
        if room_type == '1_window':
            model['Shading:Building:Detailed']['shading_1'] = {
                "idf_max_extensible_fields": 12,
                "idf_max_fields": 15,
                'transmittance_schedule_name': '',
                'number_of_vertices': 4,
                "vertices": [
                    {
                    "vertex_x_coordinate": zone_x+shading,
                    "vertex_y_coordinate": y_shading,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": y_shading,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": zone_x,
                    "vertex_y_coordinate": 0,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": zone_x+shading,
                    "vertex_y_coordinate": 0,
                    "vertex_z_coordinate": z_shading
                    }
                ]
            }
            
        if room_type == '3_window':
            model['Shading:Building:Detailed']['shading_3'] = {
                "idf_max_extensible_fields": 12,
                "idf_max_fields": 15,
                'transmittance_schedule_name': '',
                'number_of_vertices': 4,
                "vertices": [
                    {
                    "vertex_x_coordinate": -shading,
                    "vertex_y_coordinate": 0,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": 0,
                    "vertex_y_coordinate": 0,
                    "vertex_z_coordinate": z_shading
                    },
                    {
                    "vertex_x_coordinate": 0,
                    "vertex_y_coordinate": y_shading,
                    "vertex_z_coordinate": z_shading,
                    },
                    {
                    "vertex_x_coordinate": -shading,
                    "vertex_y_coordinate": y_shading,
                    "vertex_z_coordinate": z_shading
                    }
                ]
            }
         
    #### THERMAL LOADS

    model["ElectricEquipment"] = {
        "equip_office": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 11,
            "design_level_calculation_method": "Watts/Person",
            "end_use_subcategory": "General",
            "fraction_latent": 0.0,
            "fraction_lost": 0.0,
            "fraction_radiant": 0.5,
            "schedule_name": "Sch_Equip_Computador",
            "watts_per_person": 150,
            "zone_or_zonelist_name": "office"
        }
    }

    model["Lights"] = {
        "lights_office": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 11,
            "design_level_calculation_method": "Watts/Area",
            "fraction_radiant": 0.72,
            "fraction_replaceable": 1.0,
            "fraction_visible": 0.18,
            "return_air_fraction": 0.0,
            "schedule_name": "Sch_Iluminacao",
            "watts_per_zone_floor_area": lights,
            "zone_or_zonelist_name": "office"
        }
    }

    model["People"] = {
        "people_office": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 10,
            "activity_level_schedule_name": "Sch_Atividade",
            "fraction_radiant": 0.3,
            "number_of_people_calculation_method": "People/Area",
            "number_of_people_schedule_name": "Sch_Ocupacao",
            "people_per_zone_floor_area": people,
            "sensible_heat_fraction": "Autocalculate",
            "zone_or_zonelist_name": "office"
        }
    }

    #### MATERIALS

    model["Material"] = {
        "ArgamassaReboco(25mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": 1.15,
            "density": 2000.0,
            "roughness": "Rough",
            "solar_absorptance": absorptance,
            "specific_heat": 1000.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.025,
            "visible_absorptance": 0.7
        },
        "Ceram Tij 8 fur circ (10 cm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 7,
            "conductivity": .9,
            "density": 1103.0,
            "roughness": "Rough",
            "specific_heat": 920.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.033
        },
        "ForroGesso(30mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": 0.35,
            "density": 750.0,
            "roughness": "Rough",
            "solar_absorptance": 0.2,
            "specific_heat": 840.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.02,
            "visible_absorptance": 0.2
        },
        "ForroMadeira(15mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": 0.15,
            "density": 600.0,
            "roughness": "Rough",
            "solar_absorptance": 0.4,
            "specific_heat": 1340.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.015,
            "visible_absorptance": 0.4
        },
        "LajeMacicaConcreto(100mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": 1.75,
            "density": 2200.0,
            "roughness": "Rough",
            "solar_absorptance": 0.7,
            "specific_heat": 1000.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.1,
            "visible_absorptance": 0.7
        },
        "concrete": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": c_concrete,
            "density": 2200.0,
            "roughness": "Rough",
            "solar_absorptance": 0.7,
            "specific_heat": 1000.0,
            "thermal_absorptance": 0.9,
            "thickness": e_concrete,
            "visible_absorptance": 0.7
        },
        "PisoCeramico(10mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": 0.9,
            "density": 1600.0,
            "roughness": "Rough",
            "solar_absorptance": 0.6,
            "specific_heat": 920.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.01,
            "visible_absorptance": 0.6
        },
        "PortaMadeira(30mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": 0.15,
            "density": 614.0,
            "roughness": "Rough",
            "solar_absorptance": 0.9,
            "specific_heat": 2300.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.03,
            "visible_absorptance": 0.9
        },
        "TelhaCeramica": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 9,
            "conductivity": 1.05,
            "density": 2000.0,
            "roughness": "Rough",
            "solar_absorptance": 0.7,
            "specific_heat": 920.0,
            "thermal_absorptance": 0.9,
            "thickness": 0.01,
            "visible_absorptance": 0.7
        }
    }
    
    if eps:
        model['Material:NoMass'] = {
            'EPS': {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 6,
                'roughness': 'Smooth',
                'thermal_resistance': R_eps,
                'thermal_absorptance': .9,
                'solar_absorptance': absorptance,
                'visible_absorptance': .7
            }
        }

    model["Material:AirGap"] = {
        "Atico:CamaradeAr(>50mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 2,
            "thermal_resistance": 0.21
        },
        "CavidadeBloco:CamaradeAr(20-50mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 2,
            "thermal_resistance": .16
        }
    }

    model["WindowMaterial:SimpleGlazingSystem"] = {
        "Clear 3mm": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 3,
            "solar_heat_gain_coefficient": 0.8,
            "u_factor": 5.7
        },
        "glass_material_office": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 3,
            "solar_heat_gain_coefficient": glass_fs,
            "u_factor": 5.7
        }
    }
   
    with open(input_file, 'r') as file:
        seed = json.loads(file.read())
    
    if eps:
        seed["Construction"].update({
            "Exterior Wall": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 3,
                "layer_2": "concrete",
                "outside_layer": "EPS"
            }
        })
    else:
        seed["Construction"].update({
            "Exterior Wall": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 2,
                "outside_layer": "concrete"
            }
        })
        
    update(model, seed)
    
    with open(output, 'w') as file:
        file.write(json.dumps(model))

'''
main(input_file='seed_noafn.json' , output='teste_sznoafn.epJSON')
''' 
