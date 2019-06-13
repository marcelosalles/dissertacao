
import pandas as pd
from SALib.sample import saltelli

# Global variables

COL_NAMES = ['area', 'ratio', 'zone_height', 'abs', 'shading', 'azimuth',
	'wall_u', 'wall_ct', 'wwr', 'open_fac', 'thermal_loads', 'people',
    'glass', 'floor_height', 'bldg_ratio', 'room_type', 'ground', 'roof']  # 18 items.

BOUNDS = [-1, 1]

SIMULATIONS = 99978 # 76000

SAMPLE_NAME = 'sample_sobol_06-11'

def n_calc(d, n_cases):
    # N calculator

    n_size = n_cases/(2*d + 2)

    print(n_size)

    return int(n_size)


if __name__ == "__main__":

    # Define the model inputs

    cases = SIMULATIONS
    
    problem = {
        'num_vars': len(COL_NAMES),
        'names': COL_NAMES,
        'bounds': [BOUNDS for x in range(len(COL_NAMES))]
    }

    n_size = n_calc(problem['num_vars'], cases)

    # Generate samples
    param_values = saltelli.sample(problem, n_size)

    df = pd.DataFrame(param_values, columns=problem['names'])

    # Save pandas' Data Frame to a .csv file
    df.to_csv(SAMPLE_NAME+".csv", index=False)
