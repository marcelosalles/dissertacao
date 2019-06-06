
import collections
import copy
import json
import pandas as pd

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
    
def afn_surface(surface_name, open_fac=1, schedule_name="Sch_Ocupacao",
    control_mode="Temperature",component="Janela", temperature_setpoint="Temp_setpoint",
    enthalpy_difference=300000, temperature_difference=100):
    
    afn_dict = {
        "idf_max_extensible_fields": 0,
        "idf_max_fields": 12,
        "indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor": enthalpy_difference,
        "indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor": temperature_difference,
        "leakage_component_name": component,
        "surface_name": surface_name,
        "ventilation_control_mode": control_mode,
        "ventilation_control_zone_temperature_setpoint_schedule_name": schedule_name,
        "venting_availability_schedule_name": schedule_name,
        "window_door_opening_factor_or_crack_factor": open_fac
    }
    
    return(afn_dict)

def main_whole(zone_area = 10, zone_ratio = 1.5, zone_height = 3, absorptance = .5, shading = 1, azimuth = 0,
    corr_width = 2, wall_u = 2.5, wall_ct=151, corr_vent = 1, stairs = 0, zone_feat = None, concrete_eps=False,
    zones_x_floor = 6, n_floors = 1, corner_window=True, ground=False, roof=False, floor_height = 0,
    input_file = "modelo.epJSON",output = 'output.epJSON'):
    
    print(output)

    # Making sure numbers are not srings ----------

    zone_area = float(zone_area)
    zone_ratio = float(zone_ratio)
    zone_height = float(zone_height)
    floor_height = float(floor_height)
    absorptance = float(absorptance)
    shading = float(shading)
    azimuth = int(azimuth)
    corr_width = float(corr_width)
    wall_u = float(wall_u)
    zones_x_floor = int(zones_x_floor)
    n_floors = int(n_floors)

    # editing subdf thermal load

    lights = 10.5 

    # Defining U
    
    c_concrete = 1.75  # condutivity
    
    c_plaster = 1.15
    c_brick = .9
    R_air = .16
    
    if concrete_eps:
        
        e_concrete = (wall_ct*1000)/(1000*2200)  # specific heat and density
        R_concrete = e_concrete/c_concrete
        # R_eps = (1-(.17+R_concrete)*wall_u)/wall_u
        R_eps = (1-R_concrete*wall_u)/wall_u
        eps = True
        if R_eps < 0.001:
            eps = False
            # c_concrete = (wall_u*e_concrete)/(1-.17*wall_u)
            c_concrete = wall_u*e_concrete
            print('conductivity concrete: ', c_concrete)
            print('wall_u: ', wall_u, '\n', 'wall_ct: ', wall_ct)
    
    else:
        R_mat = (1-.17*wall_u)/wall_u
        c_plaster = .025/(.085227272727273 * R_mat)
        c_brick = .066/(.2875 * R_mat)
        R_air = (.62727273 * R_mat)
        
        e_concrete = .1

    # Defining dependent variabloes ----------
    zone_length = (zone_area/zone_ratio)**(1/2)
    zone_width = (zone_area /zone_length)
    n_zones = zones_x_floor * n_floors
    zones_in_sequence = int(zones_x_floor*.5)
    x0_second_row = zone_width + corr_width
    
    window_x1 = zone_width*.001
    window_x2 = zone_width*.999
    window_y1 = zone_length*.001
    window_y2 = zone_length*.999

    door_width = .9
    dist_door_wall = .1
    door_height = 2.1

    # thermal loads lists

    # electric = []
    # lights = []
    people = []

    for i in range(n_zones):
        people.append(float(zone_feat['people'][i]))

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

    # Zones --------------------

    zones_list = []

    for i in range(n_zones):
        zones_list.append( {"zone_name": 'office_'+'{:02.0f}'.format(i)} )

    for i in range(n_floors):
        zones_list.append( {"zone_name": 'corridor_'+'{:02.0f}'.format(i)} )
    offices = zones_list[:-n_floors]
    corridors = zones_list[-n_floors:]

    # x,y,z of zones' origins
    
    zn = 0
    model["Zone"] = {}

    for i in range(n_floors):
        
        y = 0

        for j in range(zones_in_sequence):
                        
            model["Zone"].update({
                # Office on the left
                "office_"+'{:02.0f}'.format(zn): {
                    "idf_max_extensible_fields": 0,
                    "idf_max_fields": 7,
                    "direction_of_relative_north": 0.0,
                    "multiplier": 1,
                    "x_origin": 0,
                    "y_origin": y,
                    "z_origin": i*zone_height +floor_height
                },
                # Office on the right
                "office_"+'{:02.0f}'.format(zn+1): {
                    "idf_max_extensible_fields": 0,
                    "idf_max_fields": 7,
                    "direction_of_relative_north": 0.0,
                    "multiplier": 1,
                    "x_origin": x0_second_row,
                    "y_origin": y,
                    "z_origin": i*zone_height +floor_height
                }
            })
            
            y += zone_length
            zn += 2
        
        model["Zone"].update({
            "corridor_"+'{:02.0f}'.format(i): {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 7,
                "direction_of_relative_north": 0.0,
                "multiplier": 1,
                "x_origin": zone_width,
                "y_origin": 0,
                "z_origin": i*zone_height +floor_height
            }
        })
   
    # Surfaces creation --------------------

    model["BuildingSurface:Detailed"] = {}

    for i in range(n_zones):

        model["BuildingSurface:Detailed"].update({
        
            # Ceiling
            "ceiling_"+'{:02.0f}'.format(i): {
                "vertices": [
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": zone_height
                    }
                ],
                "zone_name": "office_"+'{:02.0f}'.format(i)
            },

            # Floor
            "floor_"+'{:02.0f}'.format(i): {
                "surface_type": "Floor",
                "vertices": [
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": zone_width,
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
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": 0.0
                    }
                ],
                "zone_name": "office_"+'{:02.0f}'.format(i)
            },

            # Walls: 0 = up, 1 = right, 2 = down, 3 = left

            'wall_0_'+'{:02.0f}'.format(i): {
                "surface_type": "Wall",
                "vertices": [
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": zone_height
                    }
                ],
                "zone_name": "office_"+'{:02.0f}'.format(i)
            },
            "wall_1_"+'{:02.0f}'.format(i): {
                "surface_type": "Wall",
                "vertices": [
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": zone_height
                    }
                ],
                "zone_name": "office_"+'{:02.0f}'.format(i)
            },
            "wall_2_"+'{:02.0f}'.format(i): {
                "surface_type": "Wall",
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
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": zone_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": zone_height
                    }
                ],
                "zone_name": "office_"+'{:02.0f}'.format(i)
            },
            "wall_3_"+'{:02.0f}'.format(i): {
                "surface_type": "Wall",
                "vertices": [
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length,
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
                "zone_name": "office_"+'{:02.0f}'.format(i)
            }
        })
        
        # Top Condition
        if roof:  # i >= (n_zones - zones_x_floor):
            ceiling_bound = {
                "construction_name": "Exterior Roof",
                "outside_boundary_condition": "Outdoors",
                "sun_exposure": "SunExposed",
                "surface_type": "Roof",
                "wind_exposure": "WindExposed"
            }
        else:
            ceiling_bound = {
                "construction_name": "Interior Ceiling",
                "outside_boundary_condition": "Adiabatic",
                "sun_exposure": "NoSun",
                "surface_type": "Ceiling",
                "wind_exposure": "NoWind"
            }

        # Bottom condition            
        if ground:  # i < zones_x_floor:
            floor_bound = {
                "construction_name": "Exterior Floor",
                "outside_boundary_condition": "Ground",
                "sun_exposure": "NoSun",
                "wind_exposure": "NoWind"
            }
        else:
            floor_bound = {
                "construction_name": "Interior Floor",
                "sun_exposure": "NoSun",
                "wind_exposure": "NoWind",
                "outside_boundary_condition": "Adiabatic"
            }
            
        # Wall exposition condition
        exposed_wall = {
            "construction_name": "Exterior Wall",
            "outside_boundary_condition": "Outdoors",
            "sun_exposure": "SunExposed",
            "wind_exposure": "WindExposed"
        }
        interior_wall = {
            "construction_name": "Interior Wall",
            "outside_boundary_condition": "Surface",
            "sun_exposure": "NoSun",
            "wind_exposure": "NoWind"
        }
        
        if i%zones_x_floor == zones_x_floor-2 or i%zones_x_floor == zones_x_floor-1:
            wall_0_bound = exposed_wall
        else:
            wall_0_bound = copy.deepcopy(interior_wall)
            wall_0_bound.update({
                "outside_boundary_condition_object": 'wall_2_'+'{:02.0f}'.format(i+2)
            })
            
        if i%2 == 0:
            wall_1_bound = copy.deepcopy(interior_wall)
            wall_3_bound = exposed_wall
            wall_1_bound.update({
                "outside_boundary_condition_object": 'wall_corr_'+'{:02.0f}'.format(i)
            })
        else:
            wall_1_bound = exposed_wall
            wall_3_bound = copy.deepcopy(interior_wall)
            wall_3_bound.update({
                "outside_boundary_condition_object": 'wall_corr_'+'{:02.0f}'.format(i)
            })
            
        if i%zones_x_floor == 0 or i%zones_x_floor == 1:
            wall_2_bound = exposed_wall
        else:
            wall_2_bound = copy.deepcopy(interior_wall)
            wall_2_bound.update({
                "outside_boundary_condition_object": 'wall_0_'+'{:02.0f}'.format(i-2)
            })
        model["BuildingSurface:Detailed"]["ceiling_"+'{:02.0f}'.format(i)].update(ceiling_bound)
        model["BuildingSurface:Detailed"]["floor_"+'{:02.0f}'.format(i)].update(floor_bound)
        model["BuildingSurface:Detailed"]["wall_0_"+'{:02.0f}'.format(i)].update(wall_0_bound)
        model["BuildingSurface:Detailed"]["wall_1_"+'{:02.0f}'.format(i)].update(wall_1_bound)
        model["BuildingSurface:Detailed"]["wall_2_"+'{:02.0f}'.format(i)].update(wall_2_bound)
        model["BuildingSurface:Detailed"]["wall_3_"+'{:02.0f}'.format(i)].update(wall_3_bound)
        
    for i in range(n_floors):

        model["BuildingSurface:Detailed"].update({
        
            # Ceiling
            "ceiling_corr_"+'{:02.0f}'.format(i): {
                "vertices": [
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": corr_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": corr_width,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height
                    }
                ],
                "zone_name": "corridor_"+'{:02.0f}'.format(i)
            },

            # Floor
            "floor_corr_"+'{:02.0f}'.format(i): {
                "surface_type": "Floor",
                "vertices": [
                    {
                        "vertex_x_coordinate": corr_width,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": corr_width,
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
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": 0.0
                    }
                ],
                "zone_name": "corridor_"+'{:02.0f}'.format(i)
            },

            # Walls: 0 = up, 1 = right, 2 = down, 3 = left

            'wall_0_corr_'+'{:02.0f}'.format(i): {
                "surface_type": "Wall",
                "construction_name": "Exterior Wall",
                "outside_boundary_condition": "Outdoors",
                "sun_exposure": "SunExposed",
                "wind_exposure": "WindExposed",
                "vertices": [
                    {
                        "vertex_x_coordinate": corr_width,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height
                    },
                    {
                        "vertex_x_coordinate": corr_width,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": 0.0,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height
                    }
                ],
                "zone_name": "corridor_"+'{:02.0f}'.format(i)
            },
            "wall_2_corr_"+'{:02.0f}'.format(i): {
                "surface_type": "Wall",
                "construction_name": "Exterior Wall",
                "outside_boundary_condition": "Outdoors",
                "sun_exposure": "SunExposed",
                "wind_exposure": "WindExposed",
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
                        "vertex_x_coordinate": corr_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": 0.0
                    },
                    {
                        "vertex_x_coordinate": corr_width,
                        "vertex_y_coordinate": 0.0,
                        "vertex_z_coordinate": zone_height
                    }
                ],
                "zone_name": "corridor_"+'{:02.0f}'.format(i)
            }
        })
    
        for j in range(zones_in_sequence):
            
            model["BuildingSurface:Detailed"].update({
                # wall 1 (right)
                "wall_corr_"+'{:02.0f}'.format(i*zones_x_floor+j*2+1): {
                    "surface_type": "Wall",
                    "vertices": [
                        {
                            "vertex_x_coordinate": corr_width,
                            "vertex_y_coordinate": zone_length*j,
                            "vertex_z_coordinate": zone_height
                        },
                        {
                            "vertex_x_coordinate": corr_width,
                            "vertex_y_coordinate": zone_length*j,
                            "vertex_z_coordinate": 0.0
                        },
                        {
                            "vertex_x_coordinate": corr_width,
                            "vertex_y_coordinate": zone_length*(j+1),
                            "vertex_z_coordinate": 0.0
                        },
                        {
                            "vertex_x_coordinate": corr_width,
                            "vertex_y_coordinate": zone_length*(j+1),
                            "vertex_z_coordinate": zone_height
                        }
                    ],
                    "zone_name": "corridor_"+'{:02.0f}'.format(i),              
                    "construction_name": "Interior Wall",
                    "outside_boundary_condition": "Surface",
                    "outside_boundary_condition_object": 'wall_3_'+'{:02.0f}'.format(i*zones_x_floor+j*2+1),
                    "sun_exposure": "NoSun",
                    "wind_exposure": "NoWind"
                },
                # wall 3 (left)
                "wall_corr_"+'{:02.0f}'.format(i*zones_x_floor+j*2): {
                    "surface_type": "Wall",
                    "vertices": [
                        {
                            "vertex_x_coordinate": 0,
                            "vertex_y_coordinate": zone_length*(j+1),
                            "vertex_z_coordinate": zone_height
                        },
                        {
                            "vertex_x_coordinate": 0,
                            "vertex_y_coordinate": zone_length*(j+1),
                            "vertex_z_coordinate": 0.0
                        },
                        {
                            "vertex_x_coordinate": 0,
                            "vertex_y_coordinate": zone_length*j,
                            "vertex_z_coordinate": 0.0
                        },
                        {
                            "vertex_x_coordinate": 0,
                            "vertex_y_coordinate": zone_length*j,
                            "vertex_z_coordinate": zone_height
                        }
                    ],
                    "zone_name": "corridor_"+'{:02.0f}'.format(i),                    
                    "construction_name": "Interior Wall",
                    "outside_boundary_condition": "Surface",
                    "outside_boundary_condition_object": 'wall_1_'+'{:02.0f}'.format(i*zones_x_floor+j*2),
                    "sun_exposure": "NoSun",
                    "wind_exposure": "NoWind"
                },
            })
            
        # Top Condition
        if roof:  # if i == n_floors-1:
            ceiling_bound = {
                "construction_name": "Exterior Roof",
                "outside_boundary_condition": "Outdoors",
                "sun_exposure": "SunExposed",
                "surface_type": "Roof",
                "wind_exposure": "WindExposed"
            }
        else:
            ceiling_bound = {
                "construction_name": "Interior Ceiling",
                "outside_boundary_condition": "Adiabatic",
                "sun_exposure": "NoSun",
                "surface_type": "Ceiling",
                "wind_exposure": "NoWind"
            }

        # Bottom condition            
        if ground:  # if i == 0:
            floor_bound = {
                "construction_name": "Exterior Floor",
                "outside_boundary_condition": "Ground",
                "sun_exposure": "NoSun",
                "wind_exposure": "NoWind"
            }
        else:
            floor_bound = {
                "construction_name": "Interior Floor",
                "sun_exposure": "NoSun",
                "wind_exposure": "NoWind",
                "outside_boundary_condition": "Adiabatic"
            }
            
        model["BuildingSurface:Detailed"]["ceiling_corr_"+'{:02.0f}'.format(i)].update(ceiling_bound)
        model["BuildingSurface:Detailed"]["floor_corr_"+'{:02.0f}'.format(i)].update(floor_bound)
    
    for obj in model["BuildingSurface:Detailed"]:
        model["BuildingSurface:Detailed"][obj].update({
            "idf_max_extensible_fields": 12,
            "idf_max_fields": 22            
        })
            
    # FenestrationSurdace:Detailed --------------------
    open_fac_i = 0
    surface_n = 1
    model["AirflowNetwork:MultiZone:Surface"] = {}
    model["FenestrationSurface:Detailed"] = {}
        
    for i in range(n_zones):

        wwr = float(zone_feat['wwr'][i])
        window_z1 = zone_height*(1-wwr)*.5
        window_z2 = window_z1+(zone_height*wwr)
        
        if i%zones_x_floor == zones_x_floor-2: # upper left corner
            
            door_1 = True

            model["FenestrationSurface:Detailed"].update({
                "window_3_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_3_"+'{:02.0f}'.format(i),
                    "construction_name":"glass_construction_office_"+'{:02.0f}'.format(i),
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
            if corner_window == True:
                model["FenestrationSurface:Detailed"].update({
                    "window_0_"+'{:02.0f}'.format(i): {
                        "building_surface_name": "wall_0_"+'{:02.0f}'.format(i),
                        "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
                        "number_of_vertices": 4.0,
                        "surface_type": "Window",
                        "vertex_1_x_coordinate": window_x2,
                        "vertex_1_y_coordinate": zone_length,
                        "vertex_1_z_coordinate": window_z2,
                        "vertex_2_x_coordinate": window_x2,
                        "vertex_2_y_coordinate": zone_length,
                        "vertex_2_z_coordinate": window_z1,
                        "vertex_3_x_coordinate": window_x1,
                        "vertex_3_y_coordinate": zone_length,
                        "vertex_3_z_coordinate": window_z1,
                        "vertex_4_x_coordinate": window_x1,
                        "vertex_4_y_coordinate": zone_length,
                        "vertex_4_z_coordinate": window_z2
                    }
                })                
                model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_0_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
                surface_n +=1
                
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_3_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
            open_fac_i += 1
            surface_n +=1
            
        elif i%zones_x_floor == 1: # lower right corner
            
            door_1 = False

            model["FenestrationSurface:Detailed"].update({
                "window_1_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_1_"+'{:02.0f}'.format(i),
                    "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
                    "number_of_vertices": 4.0,
                    "surface_type": "Window",
                    "vertex_1_x_coordinate": zone_width,
                    "vertex_1_y_coordinate": window_y1,
                    "vertex_1_z_coordinate": window_z2,
                    "vertex_2_x_coordinate": zone_width,
                    "vertex_2_y_coordinate": window_y1,
                    "vertex_2_z_coordinate": window_z1,
                    "vertex_3_x_coordinate": zone_width,
                    "vertex_3_y_coordinate": window_y2,
                    "vertex_3_z_coordinate": window_z1,
                    "vertex_4_x_coordinate": zone_width,
                    "vertex_4_y_coordinate": window_y2,
                    "vertex_4_z_coordinate": window_z2
                }
            })
            if corner_window == True:
                model["FenestrationSurface:Detailed"].update({
                    "window_2_"+'{:02.0f}'.format(i): {
                        "building_surface_name": "wall_2_"+'{:02.0f}'.format(i),
                        "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
                        "number_of_vertices": 4.0,
                        "surface_type": "Window",
                        "vertex_1_x_coordinate": window_x1,
                        "vertex_1_y_coordinate": 0,
                        "vertex_1_z_coordinate": window_z2,
                        "vertex_2_x_coordinate": window_x1,
                        "vertex_2_y_coordinate": 0,
                        "vertex_2_z_coordinate": window_z1,
                        "vertex_3_x_coordinate": window_x2,
                        "vertex_3_y_coordinate": 0,
                        "vertex_3_z_coordinate": window_z1,
                        "vertex_4_x_coordinate": window_x2,
                        "vertex_4_y_coordinate": 0,
                        "vertex_4_z_coordinate": window_z2
                    }
                })
                model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_2_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
                surface_n +=1
                
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_1_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
            open_fac_i += 1
            surface_n += 1
            
        elif i%zones_x_floor == zones_x_floor-1: # upper right corner
            
            door_1 = False

            model["FenestrationSurface:Detailed"].update({
                "window_1_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_1_"+'{:02.0f}'.format(i),
                    "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
                    "number_of_vertices": 4.0,
                    "surface_type": "Window",
                    "vertex_1_x_coordinate": zone_width,
                    "vertex_1_y_coordinate": window_y1,
                    "vertex_1_z_coordinate": window_z2,
                    "vertex_2_x_coordinate": zone_width,
                    "vertex_2_y_coordinate": window_y1,
                    "vertex_2_z_coordinate": window_z1,
                    "vertex_3_x_coordinate": zone_width,
                    "vertex_3_y_coordinate": window_y2,
                    "vertex_3_z_coordinate": window_z1,
                    "vertex_4_x_coordinate": zone_width,
                    "vertex_4_y_coordinate": window_y2,
                    "vertex_4_z_coordinate": window_z2
                }
            })
            if corner_window == True:
                model["FenestrationSurface:Detailed"].update({
                    "window_0_"+'{:02.0f}'.format(i): {
                        "building_surface_name": "wall_0_"+'{:02.0f}'.format(i),
                        "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
                        "number_of_vertices": 4.0,
                        "surface_type": "Window",
                        "vertex_1_x_coordinate": window_x2,
                        "vertex_1_y_coordinate": zone_length,
                        "vertex_1_z_coordinate": window_z2,
                        "vertex_2_x_coordinate": window_x2,
                        "vertex_2_y_coordinate": zone_length,
                        "vertex_2_z_coordinate": window_z1,
                        "vertex_3_x_coordinate": window_x1,
                        "vertex_3_y_coordinate": zone_length,
                        "vertex_3_z_coordinate": window_z1,
                        "vertex_4_x_coordinate": window_x1,
                        "vertex_4_y_coordinate": zone_length,
                        "vertex_4_z_coordinate": window_z2
                    }
                })
                model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_0_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
                surface_n +=1
                
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_1_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
            open_fac_i += 1
            surface_n += 1
            
        elif i%zones_x_floor == 0: # lower left corner   
            
            door_1 = True

            model["FenestrationSurface:Detailed"].update({
                "window_3_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_3_"+'{:02.0f}'.format(i),
                    "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
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
            if corner_window == True:
                model["FenestrationSurface:Detailed"].update({
                    "window_2_"+'{:02.0f}'.format(i): {
                        "building_surface_name": "wall_2_"+'{:02.0f}'.format(i),
                        "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
                        "number_of_vertices": 4.0,
                        "surface_type": "Window",
                        "vertex_1_x_coordinate": window_x1,
                        "vertex_1_y_coordinate": 0,
                        "vertex_1_z_coordinate": window_z2,
                        "vertex_2_x_coordinate": window_x1,
                        "vertex_2_y_coordinate": 0,
                        "vertex_2_z_coordinate": window_z1,
                        "vertex_3_x_coordinate": window_x2,
                        "vertex_3_y_coordinate": 0,
                        "vertex_3_z_coordinate": window_z1,
                        "vertex_4_x_coordinate": window_x2,
                        "vertex_4_y_coordinate": 0,
                        "vertex_4_z_coordinate": window_z2
                    }
                })
                model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n+1)] = afn_surface("window_2_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
                surface_n +=1
                
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_3_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
            open_fac_i += 1
            surface_n += 1
            
        elif i%2 == 0: # left middle
            
            door_1 = True

            model["FenestrationSurface:Detailed"].update({
                "window_3_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_3_"+'{:02.0f}'.format(i),
                    "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
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
            
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_3_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
            open_fac_i += 1
            surface_n += 1
            
        else: # right middle
            
            door_1 = False

            model["FenestrationSurface:Detailed"].update({
                "window_1_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_1_"+'{:02.0f}'.format(i),
                    "construction_name": "glass_construction_office_"+'{:02.0f}'.format(i),
                    "number_of_vertices": 4.0,
                    "surface_type": "Window",
                    "vertex_1_x_coordinate": zone_width,
                    "vertex_1_y_coordinate": window_y1,
                    "vertex_1_z_coordinate": window_z2,
                    "vertex_2_x_coordinate": zone_width,
                    "vertex_2_y_coordinate": window_y1,
                    "vertex_2_z_coordinate": window_z1,
                    "vertex_3_x_coordinate": zone_width,
                    "vertex_3_y_coordinate": window_y2,
                    "vertex_3_z_coordinate": window_z1,
                    "vertex_4_x_coordinate": zone_width,
                    "vertex_4_y_coordinate": window_y2,
                    "vertex_4_z_coordinate": window_z2
                }
            })
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_1_"+'{:02.0f}'.format(i), float(zone_feat['open_fac'][open_fac_i]))
            open_fac_i += 1
            surface_n += 1            
        
        if door_1:
            # check if door is on wall 1 or 3
            
            model["FenestrationSurface:Detailed"].update({            
                "door_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_1_"+'{:02.0f}'.format(i),
                    "construction_name": "Interior Door",
                    "number_of_vertices": 4.0,
                    "outside_boundary_condition_object": "door_corr_"+'{:02.0f}'.format(i),
                    "surface_type": "Door",
                    "vertex_1_x_coordinate": zone_width,
                    "vertex_1_y_coordinate": zone_length-dist_door_wall-door_width,
                    "vertex_1_z_coordinate": door_height,
                    "vertex_2_x_coordinate": zone_width,
                    "vertex_2_y_coordinate": zone_length-dist_door_wall-door_width,
                    "vertex_2_z_coordinate": 0.0,
                    "vertex_3_x_coordinate": zone_width,
                    "vertex_3_y_coordinate": zone_length-dist_door_wall,
                    "vertex_3_z_coordinate": 0.0,
                    "vertex_4_x_coordinate": zone_width,
                    "vertex_4_y_coordinate": zone_length-dist_door_wall,
                    "vertex_4_z_coordinate": door_height
                }
            })
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("door_"+'{:02.0f}'.format(i), component="Porta")
            surface_n += 1
        else:
            model["FenestrationSurface:Detailed"].update({            
                "door_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_3_"+'{:02.0f}'.format(i),
                    "construction_name": "Interior Door",
                    "number_of_vertices": 4.0,
                    "outside_boundary_condition_object": "door_corr_"+'{:02.0f}'.format(i),
                    "surface_type": "Door",
                    "vertex_1_x_coordinate": 0,
                    "vertex_1_y_coordinate": zone_length-dist_door_wall,
                    "vertex_1_z_coordinate": door_height,
                    "vertex_2_x_coordinate": 0,
                    "vertex_2_y_coordinate": zone_length-dist_door_wall,
                    "vertex_2_z_coordinate": 0.0,
                    "vertex_3_x_coordinate": 0,
                    "vertex_3_y_coordinate": zone_length-dist_door_wall-door_width,
                    "vertex_3_z_coordinate": 0.0,
                    "vertex_4_x_coordinate": 0,
                    "vertex_4_y_coordinate": zone_length-dist_door_wall-door_width,
                    "vertex_4_z_coordinate": door_height
                }
            })
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("door_"+'{:02.0f}'.format(i), component="Porta")
            surface_n += 1
        
    for i in range(n_floors):
        
        for j in range(zones_in_sequence):
            
            model["FenestrationSurface:Detailed"].update({            
                "door_corr_"+'{:02.0f}'.format(i*zones_x_floor+j*2): {
                    "building_surface_name": "wall_corr_"+'{:02.0f}'.format(i*zones_x_floor+j*2),
                    "construction_name": "Interior Door",
                    "number_of_vertices": 4.0,
                    "outside_boundary_condition_object": "door_"+'{:02.0f}'.format(i*zones_x_floor+j*2),
                    "surface_type": "Door",
                    "vertex_1_x_coordinate": 0,
                    "vertex_1_y_coordinate": zone_length*(j+1)-dist_door_wall,
                    "vertex_1_z_coordinate": door_height,
                    "vertex_2_x_coordinate": 0,
                    "vertex_2_y_coordinate": zone_length*(j+1)-dist_door_wall,
                    "vertex_2_z_coordinate": 0.0,
                    "vertex_3_x_coordinate": 0,
                    "vertex_3_y_coordinate": zone_length*(j+1)-dist_door_wall-door_width,
                    "vertex_3_z_coordinate": 0.0,
                    "vertex_4_x_coordinate": 0,
                    "vertex_4_y_coordinate": zone_length*(j+1)-dist_door_wall-door_width,
                    "vertex_4_z_coordinate": door_height
                },          
                "door_corr_"+'{:02.0f}'.format(i*zones_x_floor+j*2+1): {
                    "building_surface_name": "wall_corr_"+'{:02.0f}'.format(i*zones_x_floor+j*2+1),
                    "construction_name": "Interior Door",
                    "number_of_vertices": 4.0,
                    "outside_boundary_condition_object": "door_"+'{:02.0f}'.format(i*zones_x_floor+j*2+1),
                    "surface_type": "Door",
                    "vertex_1_x_coordinate": corr_width,
                    "vertex_1_y_coordinate": zone_length*(j+1)-dist_door_wall-door_width,
                    "vertex_1_z_coordinate": door_height,
                    "vertex_2_x_coordinate": corr_width,
                    "vertex_2_y_coordinate": zone_length*(j+1)-dist_door_wall-door_width,
                    "vertex_2_z_coordinate": 0.0,
                    "vertex_3_x_coordinate": corr_width,
                    "vertex_3_y_coordinate": zone_length*(j+1)-dist_door_wall,
                    "vertex_3_z_coordinate": 0.0,
                    "vertex_4_x_coordinate": corr_width,
                    "vertex_4_y_coordinate": zone_length*(j+1)-dist_door_wall,
                    "vertex_4_z_coordinate": door_height
                }
            })
            
        # corridor ventilation 

        if corr_vent > 0:
            
            model["FenestrationSurface:Detailed"].update({
                "window_0_corr_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_0_corr_"+'{:02.0f}'.format(i),
                    "construction_name": "Exterior Window",
                    "number_of_vertices": 4.0,
                    "surface_type": "Window",
                    "vertex_1_x_coordinate": corr_width*.75,
                    "vertex_1_y_coordinate": zone_length*zones_in_sequence,
                    "vertex_1_z_coordinate": door_height,
                    "vertex_2_x_coordinate": corr_width*.75,
                    "vertex_2_y_coordinate": zone_length*zones_in_sequence,
                    "vertex_2_z_coordinate": door_height-1,
                    "vertex_3_x_coordinate": corr_width*.25,
                    "vertex_3_y_coordinate": zone_length*zones_in_sequence,
                    "vertex_3_z_coordinate": door_height-1,
                    "vertex_4_x_coordinate": corr_width*.25,
                    "vertex_4_y_coordinate": zone_length*zones_in_sequence,
                    "vertex_4_z_coordinate": door_height
                },
                "window_2_corr_"+'{:02.0f}'.format(i): {
                    "building_surface_name": "wall_2_corr_"+'{:02.0f}'.format(i),
                    "construction_name": "Exterior Window",
                    "number_of_vertices": 4.0,
                    "surface_type": "Window",
                    "vertex_1_x_coordinate": corr_width*.25,
                    "vertex_1_y_coordinate": 0,
                    "vertex_1_z_coordinate": door_height,
                    "vertex_2_x_coordinate": corr_width*.25,
                    "vertex_2_y_coordinate": 0,
                    "vertex_2_z_coordinate": door_height-1,
                    "vertex_3_x_coordinate": corr_width*.75,
                    "vertex_3_y_coordinate": 0,
                    "vertex_3_z_coordinate": door_height-1,
                    "vertex_4_x_coordinate": corr_width*.75,
                    "vertex_4_y_coordinate": 0,
                    "vertex_4_z_coordinate": door_height
                }
            })
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("window_0_corr_"+'{:02.0f}'.format(i))
            model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n+1)] = afn_surface("window_2_corr_"+'{:02.0f}'.format(i))
            surface_n += 2  

        # Stairs

        if stairs > 0:

            if i > 0: # not ground floor
            
                model["FenestrationSurface:Detailed"].update({
                    "stair_inf_"+'{:02.0f}'.format(i): {
                        "building_surface_name": "floor_corr_"+'{:02.0f}'.format(i),
                        "outside_boundary_condition_object": "stair_sup_"+'{:02.0f}'.format(i-1),
                        "construction_name": "InfraRed",
                        "number_of_vertices": 4.0,
                        "surface_type": "Door",
                        "vertex_1_x_coordinate": 0.99*corr_width,
                        "vertex_1_y_coordinate": 0.01,
                        "vertex_1_z_coordinate": 0,
                        "vertex_2_x_coordinate": 0.01*corr_width,
                        "vertex_2_y_coordinate": 0.01,
                        "vertex_2_z_coordinate": 0,
                        "vertex_3_x_coordinate": 0.01*corr_width,
                        "vertex_3_y_coordinate": 4.51,
                        "vertex_3_z_coordinate": 0,
                        "vertex_4_x_coordinate": 0.99*corr_width,
                        "vertex_4_y_coordinate": 4.51,
                        "vertex_4_z_coordinate": 0
                    }
                })

            if i < n_floors-1: # not roof floor
                model["FenestrationSurface:Detailed"].update({
                    "stair_sup_"+'{:02.0f}'.format(i): {
                        "building_surface_name": "ceiling_corr_"+'{:02.0f}'.format(i),
                        "outside_boundary_condition_object": "stair_inf_"+'{:02.0f}'.format(i+1),
                        "construction_name": "InfraRed",
                        "number_of_vertices": 4.0,
                        "surface_type": "Door",
                        "vertex_1_x_coordinate": 0.01*corr_width,
                        "vertex_1_y_coordinate": 0.01,
                        "vertex_1_z_coordinate": zone_height,
                        "vertex_2_x_coordinate": 0.99*corr_width,
                        "vertex_2_y_coordinate": 0.01,
                        "vertex_2_z_coordinate": zone_height,
                        "vertex_3_x_coordinate": 0.99*corr_width,
                        "vertex_3_y_coordinate": 4.51,
                        "vertex_3_z_coordinate": zone_height,
                        "vertex_4_x_coordinate": 0.01*corr_width,
                        "vertex_4_y_coordinate": 4.51,
                        "vertex_4_z_coordinate": zone_height
                    }
                })
                model["AirflowNetwork:MultiZone:Surface"]["AirflowNetwork:MultiZone:Surface "+str(surface_n)] = afn_surface("stair_sup_"+'{:02.0f}'.format(i), component="HorizontalOpening",
                schedule_name="Always On", control_mode="Constant")
            surface_n += 1
    
    for obj in model["FenestrationSurface:Detailed"]:
        model["FenestrationSurface:Detailed"][obj].update({
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 22            
        })

    # Shading ----------------------------------------------------
 
    if shading > 0.01:
 
        # Shading:Building:Detailed
 
        model['Shading:Building:Detailed'] = {}
 
        for i in range(n_floors):

            model['Shading:Building:Detailed'].update({
                'shading_0_'+'{:02.0f}'.format(i): {
                    "idf_max_extensible_fields": 12,
                    "idf_max_fields": 15,
                    'transmittance_schedule_name': '',
                    'number_of_vertices': 4,
                    "vertices": [
                        {
                        "vertex_x_coordinate": 0,
                        "vertex_y_coordinate": zone_length*zones_in_sequence+shading,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 0,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width,
                        "vertex_y_coordinate": zone_length*zones_in_sequence+shading,
                        "vertex_z_coordinate": zone_height*(i+1)
                        }
                    ]
                },
                'shading_1_'+'{:02.0f}'.format(i): {
                    "idf_max_extensible_fields": 12,
                    "idf_max_fields": 15,
                    'transmittance_schedule_name': '',
                    'number_of_vertices': 4,
                    "vertices": [
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width+shading,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width,
                        "vertex_y_coordinate": 0,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width+shading,
                        "vertex_y_coordinate": 0,
                        "vertex_z_coordinate": zone_height*(i+1)
                        }
                    ]
                },
                'shading_2_'+'{:02.0f}'.format(i): {
                    "idf_max_extensible_fields": 12,
                    "idf_max_fields": 15,
                    'transmittance_schedule_name': '',
                    'number_of_vertices': 4,
                    "vertices": [
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width,
                        "vertex_y_coordinate": -shading,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 2*zone_width+corr_width,
                        "vertex_y_coordinate": 0,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 0,
                        "vertex_y_coordinate": 0,
                        "vertex_z_coordinate": zone_height*(i+1),
                        },
                        {
                        "vertex_x_coordinate": 0,
                        "vertex_y_coordinate": -shading,
                        "vertex_z_coordinate": zone_height*(i+1)
                        }
                    ]
                },
                'shading_3_'+'{:02.0f}'.format(i): {
                    "idf_max_extensible_fields": 12,
                    "idf_max_fields": 15,
                    'transmittance_schedule_name': '',
                    'number_of_vertices': 4,
                    "vertices": [
                        {
                        "vertex_x_coordinate": -shading,
                        "vertex_y_coordinate": 0,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 0,
                        "vertex_y_coordinate": 0,
                        "vertex_z_coordinate": zone_height*(i+1)
                        },
                        {
                        "vertex_x_coordinate": 0,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height*(i+1),
                        },
                        {
                        "vertex_x_coordinate": -shading,
                        "vertex_y_coordinate": zone_length*zones_in_sequence,
                        "vertex_z_coordinate": zone_height*(i+1)
                        }
                    ]
                }
            })
    
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
            "zone_or_zonelist_name": "Offices"
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
            "zone_or_zonelist_name": "Offices"
        }
    }
    
    model["WindowMaterial:SimpleGlazingSystem"] = {
        "Clear 3mm": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 3,
            "solar_heat_gain_coefficient": 0.8,
            "u_factor": 5.7
        }
    }
    model["Construction"] = {}
    model["People"] = {}
    
    for i in range(len(offices)):
        
        model["People"].update({
            "people_office_"+'{:02.0f}'.format(i): {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 10,
                "activity_level_schedule_name": "Sch_Atividade",
                "fraction_radiant": 0.3,
                "number_of_people_calculation_method": "People/Area",
                "number_of_people_schedule_name": "Sch_Ocupacao",
                "people_per_zone_floor_area": people[i],
                "sensible_heat_fraction": "Autocalculate",
                "zone_or_zonelist_name": "office_"+'{:02.0f}'.format(i)
            }
        })
        
        model["WindowMaterial:SimpleGlazingSystem"].update({
            "glass_material_office_"+'{:02.0f}'.format(i): {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 3,
                "solar_heat_gain_coefficient": float(zone_feat['glass'][i]),
                "u_factor": 5.7
            }
        })
        
        model["Construction"].update({
            "glass_construction_office_"+'{:02.0f}'.format(i): {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 2,
                "outside_layer": "glass_material_office_"+'{:02.0f}'.format(i)
            }
        })
        
    model["ZoneList"] = {
        "All": {
            "idf_max_extensible_fields": len(zones_list),
            "idf_max_fields": len(zones_list)+1,
            "zones": zones_list
        },
        'Offices': {
            "idf_max_extensible_fields": len(offices),
            "idf_max_fields": len(offices)+1,
            "zones": offices
        },
        'Corridors': {
            "idf_max_extensible_fields": len(corridors),
            "idf_max_fields": len(corridors)+1,
            "zones": corridors
        }
    }

    model['AirflowNetwork:MultiZone:Zone'] = {}
    zone_n = 1
    for i in range(len(zones_list)):
        
        model['AirflowNetwork:MultiZone:Zone'].update({
            "AirflowNetwork:MultiZone:Zone "+str(zone_n): {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 8,
                "indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor": 300000.0,
                "indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor": 100.0,
                "zone_name": model["ZoneList"]["All"]['zones'][i]['zone_name']
            }
        })
        zone_n += 1
       
    if stairs > 0:
        
        model["AirflowNetwork:MultiZone:Component:HorizontalOpening"] = {
            "HorizontalOpening": {
                "air_mass_flow_coefficient_when_opening_is_closed": 0.001,
                "air_mass_flow_exponent_when_opening_is_closed": 0.65,
                "discharge_coefficient": 0.6,
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "sloping_plane_angle": 25.0
            }
        }
    
    # AFN Simulation Control
    bldg_ratio = (2*zone_width+corr_width)/(zones_in_sequence*zone_length)
    if bldg_ratio <= 1:
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
            "height_selection_for_local_wind_pressure_calculation": "OpeningHeight",
            "initialization_type": "ZeroNodePressures",
            "maximum_number_of_iterations": 500,
            "ratio_of_building_width_along_short_axis_to_width_along_long_axis": bldg_ratio,
            "relative_airflow_convergence_tolerance": 0.01,
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 12,
            "wind_pressure_coefficient_type": "SurfaceAverageCalculation"
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
    
    model["Material:AirGap"] = {
        "CavidadeBloco:CamaradeAr(20-50mm)": {
            "idf_max_extensible_fields": 0,
            "idf_max_fields": 2,
            "idf_order": 30,
            "thermal_resistance": R_air
        }
    }
    
    if concrete_eps:
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
       
    with open(input_file, 'r') as file:
        seed = json.loads(file.read())
    
    if concrete_eps:
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
    
    complete_model = update(seed, model)
    
    with open(output, 'w') as file:
        file.write(json.dumps(complete_model))
   
'''  

zone_feat = {
    'people': [],
    'wwr': [],
    'open_fac': [],
    'glass': []
}
    
for i in range(6):
    zone_feat['people'].append(.5)
    zone_feat['wwr'].append(.5)
    zone_feat['open_fac'].append(.5)
    zone_feat['glass'].append(.5)

main_whole(zone_area = 10, zone_ratio = 1.5, zone_height = 3, absorptance = .5, shading = 1, azimuth = 0,
    corr_width = 2, wall_u = 2.5, wall_ct=100, corr_vent = 1, stairs = 0, zone_feat = zone_feat, concrete_eps=False,
    zones_x_floor = 6, n_floors = 1, corner_window=True, ground=False, roof=False, floor_height = 0,
    input_file = "seed_single.json",output = 'teste_whole-floor.epJSON')
'''
