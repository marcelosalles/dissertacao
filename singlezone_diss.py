# The names given to the surfaces go from 0 to 3, being 0 up, 1 right,
# 2 down, 3 left. 

from cp_calc import cp_calc
import collections
import json
import numpy as np

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
    people=.1, glass_fs=.87, wwr=.6, door=True, cp_eq = True,
    open_fac=.5, input_file='seed.json' , output='output.epJSON'):
    
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
    open_fac = float(open_fac)
    
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
            "outside_boundary_condition": "Adiabatic",
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

    if door:
        model["FenestrationSurface:Detailed"].update({
            "door_office": {
                "building_surface_name": "wall-2_office",
                "construction_name": "Interior Door",
                "number_of_vertices": 4.0,
                "surface_type": "Door",
                "vertex_1_x_coordinate": dist_door_wall,
                "vertex_1_y_coordinate": 0,
                "vertex_1_z_coordinate": door_height,
                "vertex_2_x_coordinate": dist_door_wall,
                "vertex_2_y_coordinate": 0,
                "vertex_2_z_coordinate": 0.0,
                "vertex_3_x_coordinate": dist_door_wall+door_width,
                "vertex_3_y_coordinate": 0,
                "vertex_3_z_coordinate": 0.0,
                "vertex_4_x_coordinate": dist_door_wall+door_width,
                "vertex_4_y_coordinate": 0,
                "vertex_4_z_coordinate": door_height
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
    
    
    if shading > 1:
		
        shading_length = np.tan((np.pi*shading)/180) * (wwr*zone_height)
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
                    "vertex_y_coordinate": y_shading+shading_length,
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
                    "vertex_y_coordinate": y_shading+shading_length,
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
                    "vertex_x_coordinate": zone_x+shading_length,
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
                    "vertex_x_coordinate": zone_x+shading_length,
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
                    "vertex_x_coordinate": -shading_length,
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
                    "vertex_x_coordinate": -shading_length,
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

    #### AFN OBJECTS

    # AFN Simulation Control
    if bldg_ratio <= 1:  # x/y
        wind_azimuth = azimuth%180
    else:
        bldg_ratio = 1/bldg_ratio
        wind_azimuth = (azimuth+90)%180
        
    model["AirflowNetwork:SimulationControl"] = {
        "Ventilacao": {
            "absolute_airflow_convergence_tolerance": 0.0001,
            "airflownetwork_control": "MultizoneWithoutDistribution",
            "azimuth_angle_of_long_axis_of_building": wind_azimuth,
            "building_type": "HighRise",
            "convergence_acceleration_limit": -0.5,
            "height_selection_for_local_wind_pressure_calculation": "ExternalNode",
            "initialization_type": "ZeroNodePressures",
            "maximum_number_of_iterations": 500,
            "ratio_of_building_width_along_short_axis_to_width_along_long_axis": bldg_ratio,
            "relative_airflow_convergence_tolerance": 0.01,
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 12,
            "wind_pressure_coefficient_type": "Input"
        }
    }

    # AFN Zone
    model["AirflowNetwork:MultiZone:Zone"] = {
        "AirflowNetwork:MultiZone:Zone 1": {
            "indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor": 300000.0,
            "indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor": 100.0,
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 8,
            "zone_name": "office"
        }
    }

    # AFN Surface
    model["AirflowNetwork:MultiZone:Surface"] = {
        "AirflowNetwork:MultiZone:Surface 1": {
            "external_node_name": "window_0_office_Node",
            "indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor": 300000.0,
            "indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor": 100.0,
            "leakage_component_name": "Janela",
            "surface_name": "window_0_office",
            "ventilation_control_mode": "Temperature",
            "ventilation_control_zone_temperature_setpoint_schedule_name": "Temp_setpoint",
            "venting_availability_schedule_name": "Sch_Ocupacao",
            "window_door_opening_factor_or_crack_factor": open_fac
        },
        "AirflowNetwork:MultiZone:Surface 2": {
            "external_node_name": "door_office_Node",
            "indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor": 300000.0,
            "indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor": 100.0,
            "leakage_component_name": "door_crack",
            "surface_name": "wall-0_office"
        }
    }

    if room_type == '3_window' or room_type == '1_window':

        model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface 3"] = {
            "external_node_name": "window_side_office_Node",
            "indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor": 300000.0,
            "indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor": 100.0,
            "leakage_component_name": "Janela",
            "surface_name": "window_side_office",
            "ventilation_control_mode": "Temperature",
            "ventilation_control_zone_temperature_setpoint_schedule_name": "Temp_setpoint",
            "venting_availability_schedule_name": "Sch_Ocupacao",
            "window_door_opening_factor_or_crack_factor": open_fac
        }
    
    for obj in model["AirflowNetwork:MultiZone:Surface"]:
        
        model["AirflowNetwork:MultiZone:Surface"][obj].update({
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 12
        })
        
    model["AirflowNetwork:MultiZone:ExternalNode"] = {
        "window_0_office_Node": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 5,
            "external_node_height": floor_height+.5*zone_height,
            "symmetric_wind_pressure_coefficient_curve": "No",
            "wind_angle_type": "Absolute",
            "wind_pressure_coefficient_curve_name": "window_0_office_coef"
        },
        "door_office_Node": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 5,
            "external_node_height": floor_height+.5*zone_height,
            "symmetric_wind_pressure_coefficient_curve": "No",
            "wind_angle_type": "Absolute",
            "wind_pressure_coefficient_curve_name": "door_office_coef"
        }
    }
    if room_type == '3_window' or room_type == '1_window':
        model["AirflowNetwork:MultiZone:ExternalNode"]["window_side_office_Node"] = {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 5,
            "external_node_height": floor_height+.5*zone_height,
            "symmetric_wind_pressure_coefficient_curve": "No",
            "wind_angle_type": "Absolute",
            "wind_pressure_coefficient_curve_name": "window_side_office_coef"
        }
        
    model["AirflowNetwork:MultiZone:WindPressureCoefficientArray"] = {
        "ventos": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 13,
            "wind_direction_1": 0.0,
            "wind_direction_2": 30.0,
            "wind_direction_3": 60.0,
            "wind_direction_4": 90.0,
            "wind_direction_5": 120.0,
            "wind_direction_6": 150.0,
            "wind_direction_7": 180.0,
            "wind_direction_8": 210.0,
            "wind_direction_9": 240.0,
            "wind_direction_10": 270.0,
            "wind_direction_11": 300.0,
            "wind_direction_12": 330.0
        }
    }
        
    model["AirflowNetwork:MultiZone:WindPressureCoefficientValues"] = cp_calc(bldg_ratio, azimuth=azimuth, room_type=room_type, cp_eq=cp_eq, zone_x=zone_x, zone_y=zone_y, wwr=wwr, zn=zn,corner_window=corner_window)
        
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
main(zone_area=8.85, zone_ratio=1.18, zone_height=2.5, absorptance=.5,
    shading=0.5, azimuth=180, bldg_ratio=0.85, wall_u=4.083, wall_ct=165.6,
    zn=0, floor_height=0, corner_window=False, ground=1,
    roof=1, people=.226, glass_fs=.87, wwr=.219, open_fac=0.45, 
    input_file='seed_single_U-conc-eps.json' , output='dorm1.epJSON')
      
main(zone_area=8.3, zone_ratio=.9, zone_height=2.5, absorptance=.5,
    shading=0.5, azimuth=90, bldg_ratio=0.85, wall_u=4.083, wall_ct=165.6,
    zn=5, floor_height=0, corner_window=False, ground=1,
    roof=1, people=.241, glass_fs=.87, wwr=.198, open_fac=0.45, 
    input_file='seed_single_U-conc-eps.json' , output='dorm2.epJSON')
      
main(zone_area=21.43, zone_ratio=.55, zone_height=2.5, absorptance=.5,
    shading=0.5, azimuth=270, bldg_ratio=0.85, wall_u=4.083, wall_ct=165.6,
    zn=0, floor_height=0, corner_window=True, ground=1,
    roof=1, people=.187, glass_fs=.87, wwr=.123, open_fac=0.45, 
    input_file='seed_single_U-conc-eps.json' , output='sala.epJSON')
  
''' '''         
main(zone_area=25, zone_ratio=1, zone_height=3, absorptance=.8,
    shading=0, azimuth=0, bldg_ratio=1, wall_u=.5, wall_ct=30,
    zn=2, floor_height=0, corner_window=False, ground=0,
    roof=0, people=.01, glass_fs=.87, wwr=.6, open_fac=0.1, 
    input_file='seed_single_U-conc-eps.json' , output='ct_baixo_0.epJSON')
main(zone_area=25, zone_ratio=1, zone_height=3, absorptance=.8,
    shading=0, azimuth=0, bldg_ratio=1, wall_u=4, wall_ct=30,
    zn=2, floor_height=0, corner_window=False, ground=0,
    roof=0, people=.01, glass_fs=.87, wwr=.6, open_fac=0.1, 
    input_file='seed_single_U-conc-eps.json' , output='ct_baixo_1.epJSON')
main(zone_area=25, zone_ratio=1, zone_height=3, absorptance=.8,
    shading=0, azimuth=0, bldg_ratio=1, wall_u=.5, wall_ct=300,
    zn=2, floor_height=0, corner_window=False, ground=0,
    roof=0, people=.01, glass_fs=.87, wwr=.6, open_fac=0.1, 
    input_file='seed_single_U-conc-eps.json' , output='ct_alto_0.epJSON')
main(zone_area=25, zone_ratio=1, zone_height=3, absorptance=.8,
    shading=0, azimuth=0, bldg_ratio=1, wall_u=4, wall_ct=300,
    zn=2, floor_height=0, corner_window=False, ground=0,
    roof=0, people=.01, glass_fs=.87, wwr=.6, open_fac=0.1, 
    input_file='seed_single_U-conc-eps.json' , output='ct_alto_1.epJSON')

main(zone_area=15, zone_ratio=1, zone_height=3, absorptance=.2,
    shading=1, azimuth=90, bldg_ratio=1, wall_u=2.5, wall_ct=100,
    zn=2, floor_height=10, corner_window=True, ground=0,
    roof=0, people=.1, glass_fs=.87, wwr=.3, open_fac=1, 
    input_file='seed_single_U-conc-eps.json' , output='azimute_90.epJSON')
    
main(zone_area=15, zone_ratio=1, zone_height=3, absorptance=.2,
    shading=1, azimuth=180, bldg_ratio=1, wall_u=2.5, wall_ct=100,
    zn=2, floor_height=10, corner_window=True, ground=0,
    roof=0, people=.1, glass_fs=.87, wwr=.3, open_fac=1, 
    input_file='seed_single_U-conc-eps.json' , output='azimute_180.epJSON')
    
main(zone_area=15, zone_ratio=1, zone_height=3, absorptance=.2,
    shading=1, azimuth=270, bldg_ratio=1, wall_u=2.5, wall_ct=100,
    zn=2, floor_height=10, corner_window=True, ground=0,
    roof=0, people=.1, glass_fs=.87, wwr=.3, open_fac=1, 
    input_file='seed_single_U-conc-eps.json' , output='azimute_270.epJSON')
''' 
