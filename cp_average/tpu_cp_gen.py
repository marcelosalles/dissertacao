import json
import pandas as pd

df = pd.read_csv('TPU_212_cp.csv')

for nfloor in range(8):
    
    tpu_dict = {
        "AirflowNetwork:SimulationControl": {
            "Ventilacao": {
                "absolute_airflow_convergence_tolerance": 0.0001,
                "airflownetwork_control": "MultizoneWithoutDistribution",
                "azimuth_angle_of_long_axis_of_building": 90,
                "building_type": "HighRise",
                "convergence_acceleration_limit": -0.5,
                "height_selection_for_local_wind_pressure_calculation": "ExternalNode",
                "initialization_type": "ZeroNodePressures",
                "maximum_number_of_iterations": 500,
                "ratio_of_building_width_along_short_axis_to_width_along_long_axis": 0.7947869038423273,
                "relative_airflow_convergence_tolerance": 0.01,
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 12,
                "wind_pressure_coefficient_type": "Input"
            }
        },
        "AirflowNetwork:MultiZone:ExternalNode": {
            "window_2_00_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_2_00_curve"
            },
            "window_3_00_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_3_00_curve"
            },
            "window_1_01_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_1_01_curve"
            },
            "window_2_01_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_2_01_curve"
            },
            "window_3_02_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_3_02_curve"
            },
            "window_1_03_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_1_03_curve"
            },
            "window_0_04_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_0_04_curve"
            },
            "window_3_04_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_3_04_curve"
            },
            "window_0_05_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_0_05_curve"
            },
            "window_1_05_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_1_05_curve"
            },
            "window_0_corr_00_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_corr_curve"
            },
            "window_2_corr_00_Node": {
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 5,
                "external_node_height": 1.5+3*nfloor,
                "symmetric_wind_pressure_coefficient_curve": "No",
                "wind_angle_type": "Relative",
                "wind_pressure_coefficient_curve_name": "window_corr_curve"
            } 
        },
        "AirflowNetwork:MultiZone:WindPressureCoefficientArray": {
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
            ,
        "AirflowNetwork:MultiZone:WindPressureCoefficientValues": {
            "window_2_00_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 3) & (df.floor == nfloor),'cp'])
            },
            "window_3_00_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 2) & (df.floor == nfloor),'cp'])
            },
            "window_1_01_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 0) & (df.floor == nfloor),'cp'])
            },
            "window_2_01_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 5) & (df.floor == nfloor),'cp'])
            },
            "window_3_02_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 1) & (df.floor == nfloor),'cp'])
            },
            "window_1_03_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 1) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 1) & (df.floor == nfloor),'cp'])
            },
            "window_0_04_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 5) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 5) & (df.floor == nfloor),'cp'])
            },
            "window_3_04_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 0) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 0) & (df.floor == nfloor),'cp'])
            },
            "window_0_05_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 3) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 3) & (df.floor == nfloor),'cp'])
            },
            "window_1_05_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 2) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 2) & (df.floor == nfloor),'cp'])
            },
            "window_corr_curve": {
                "airflownetwork_multizone_windpressurecoefficientarray_name": "ventos",
                "idf_max_extensible_fields": 0,
                "idf_max_fields": 14,
                "wind_pressure_coefficient_value_1": float(df.loc[(df.angle == 0) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_2": float(df.loc[(df.angle == 30) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_3": float(df.loc[(df.angle == 60) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_4": float(df.loc[(df.angle == 90) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_5": float(df.loc[(df.angle == 120) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_6": float(df.loc[(df.angle == 150) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_7": float(df.loc[(df.angle == 180) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_8": float(df.loc[(df.angle == 210) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_9": float(df.loc[(df.angle == 240) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_10": float(df.loc[(df.angle == 270) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_11": float(df.loc[(df.angle == 300) & (df.zone == 4) & (df.floor == nfloor),'cp']),
                "wind_pressure_coefficient_value_12": float(df.loc[(df.angle == 330) & (df.zone == 4) & (df.floor == nfloor),'cp'])
            }
        }
    }
    
    with open('tpu_floor'+str(nfloor)+'.json', 'w') as file:
        file.write(json.dumps(tpu_dict))

'''    
'''
    
