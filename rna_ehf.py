# -*- coding: utf-8 -*-
"""RNA_EHF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12DZDRnWWf_HuGFCqKwwQ_cea4_lNXbh2

# Rede Neural Artificial - Edificações de Escritórios

Código para desenvolvimento de uma RNA para predição de fração de horas em conforto em Edificações de Escritório com ventilação natural.

## _Neural Networks - Office Buildings_
_Development of a ANN to estimate thermal comfort Exceedance Hour Fraction (EHF) in naturally ventilated office buildings._

## 1. Importação das bibiliotecas
### _1. Import libraries_
"""

from __future__ import print_function

from google.colab import files

import math

from IPython import display
from matplotlib import cm
from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
import tensorflow as tf
from tensorflow.python.data import Dataset

tf.logging.set_verbosity(tf.logging.ERROR)
pd.options.display.max_rows = 18
pd.options.display.float_format = '{:.2f}'.format

from datetime import datetime

"""## 2. Importação dos dados
### _3. Import data_
"""

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

dataset = pd.read_csv('dataset_08-14.csv')
dataset = dataset.reindex(
    np.random.permutation(dataset.index))

dataset_validation = pd.read_csv('dataset_validation08-14.csv')
dataset_validation = dataset_validation.reindex(
    np.random.permutation(dataset_validation.index))

dataset_test = pd.read_csv('dataset_test_08-14b.csv')
dataset_test = dataset_test.reindex(
    np.random.permutation(dataset_test.index))

def preprocess_features(dataset, features, lhs_to_sobol=False):
  """Prepares input features from dataset.

  Args:
    dataset: A Pandas DataFrame with the dataset.
    features: A list of strings with the features names.
  Returns:
    A DataFrame that contains the features to be used for the model.
  """
  selected_features = dataset[features]
  processed_features = selected_features.copy()
  
  if lhs_to_sobol:
    processed_features = processed_features*2-1
  
  return processed_features

def preprocess_targets(dataset, target):
  """Prepares target features (i.e., labels) from data set.

  Args:
    dataset: A Pandas DataFrame with the dataset.
    targets: A string with the target name.
  Returns:
    A DataFrame that contains the target feature.
  """
  output_targets = pd.DataFrame()
  output_targets[target] = dataset[target]
  
  return output_targets

print(list(dataset))
print(list(dataset_validation))
print(list(dataset_test))

# Define the feature names and the target
features = ['area', 'azimuth', 'floor_height', 'absorptance', 'wall_u', 'wwr', 
            'shading', 'people', 'open_fac', 'roof', 'ground', 'v_ar',
            'glass', 'room_type']

target = 'ehf'

dataset_features = preprocess_features(dataset,features,
                                       lhs_to_sobol=True)  # False)  # 
dataset_targets = preprocess_targets(dataset,target)

dataset_validation_features = preprocess_features(dataset_validation,features, 
                                                  lhs_to_sobol=True)
dataset_validation_targets = preprocess_targets(dataset_validation,target)

dataset_test_features = preprocess_features(dataset_test,features, 
                                                  lhs_to_sobol=True)  # False)  # 
dataset_test_targets = preprocess_targets(dataset_test,target)


# Double-check that we've done the right thing.
print("Features summary:")
display.display(dataset_features.describe())
print("Target summary:")
display.display(dataset_targets.describe())

"""## 3. Análise de correlação
### _3. Correlation analysis_
"""

correlation_dataframe = dataset_features.copy()
correlation_dataframe["target"] = dataset_targets[target]

correlation_dataframe.corr()

"""## 4. Normalização dos dados
### _4. Data normalization_
"""

# Check features' histograms.

_ = dataset_features.hist(bins=20, figsize=(18, 12), xlabelsize=10)

# Check targets' histogram.

_ = dataset_targets.hist(bins=20, figsize=(18, 12), xlabelsize=10)

# Functions to normalize the data.
def linear_scale(series):
  min_val = series.min()
  max_val = series.max()
  scale = (max_val - min_val) / 2.0
  return series.apply(lambda x:((x - min_val) / scale) - 1.0)

def log_normalize(series, base = 10):
  return series.apply(lambda x:math.log(x+1.0, base))

def inv_log_normalize(series, base = 10):
  return series.apply(lambda x:math.log(1/(x+1.0), base))

def pow_normalize(series, base=1/2):
  return series.apply(lambda x:math.pow(x, base))

def sigmoid_normalize(series):
  return series.apply(lambda x:1/(1+math.exp(-x)))

def tan_normalize(series):
  return series.apply(lambda x:math.tan(x))

def asinh_normalize(series):
  return series.apply(lambda x:math.asinh(x))

def atan_normalize(series):
  return series.apply(lambda x:math.atan(x))

def clip(series, clip_to_min, clip_to_max):
  return series.apply(lambda x:(
    min(max(x, clip_to_min), clip_to_max)))

def z_score_normalize(series):
  mean = series.mean()
  std_dv = series.std()
  return series.apply(lambda x:(x - mean) / std_dv)

def binary_threshold(series, threshold):
  return series.apply(lambda x:(1 if x > threshold else 0))

def get_quantile_based_buckets(feature_values, num_buckets):
  quantiles = feature_values.quantile(
    [(i+1.)/(num_buckets + 1.) for i in range(num_buckets)])
  return [quantiles[q] for q in quantiles.keys()]

## Training dataset

dataset_features['roof'] = binary_threshold(dataset_features['roof'], .6)  # 0)
dataset_features['ground'] = binary_threshold(dataset_features['ground'], .7)  # 0)

# room_type from num to factor
string_roomtype = dataset_features['room_type'].apply(lambda x: '0_window')
string_roomtype[dataset_features['room_type'] < .6] = '3_wall'
string_roomtype[dataset_features['room_type'] < .2] = '1_wall'
string_roomtype[dataset_features['room_type'] < -.2] = '3_window'
string_roomtype[dataset_features['room_type'] < -.6] = '1_window'
dataset_features['room_type'] = string_roomtype

# v_ar to discrete
string_v_ar = dataset_features['v_ar'].apply(lambda x: .5)  
string_v_ar[dataset_features['v_ar'] < .5] = 0
string_v_ar[dataset_features['v_ar'] < 0] = -.5
string_v_ar[dataset_features['v_ar'] < -.5] = -1
dataset_features['v_ar'] = string_v_ar

# Validation dataset

dataset_validation_features['roof'] = binary_threshold(dataset_validation_features['roof'], .6)  # 0)
dataset_validation_features['ground'] = binary_threshold(dataset_validation_features['ground'], .7)  # 0)

# room_type from num to factor
string_roomtype = dataset_validation_features['room_type'].apply(lambda x: '0_window')  
string_roomtype[dataset_validation_features['room_type'] < .6] = '3_wall'
string_roomtype[dataset_validation_features['room_type'] < .2] = '1_wall'
string_roomtype[dataset_validation_features['room_type'] < -.2] = '3_window'
string_roomtype[dataset_validation_features['room_type'] < -.6] = '1_window'
dataset_validation_features['room_type'] = string_roomtype

# v_ar to discrete
string_v_ar = dataset_validation_features['v_ar'].apply(lambda x: .5)  
string_v_ar[dataset_validation_features['v_ar'] < .5] = 0
string_v_ar[dataset_validation_features['v_ar'] < 0] = -.5
string_v_ar[dataset_validation_features['v_ar'] < -.5] = -1
dataset_validation_features['v_ar'] = string_v_ar

# Test dataset

dataset_test_features['roof'] = binary_threshold(dataset_test_features['roof'], .6)  # 0)
dataset_test_features['ground'] = binary_threshold(dataset_test_features['ground'], .7)  # 0)

# room_type from num to factor
string_roomtype = dataset_test_features['room_type'].apply(lambda x: '0_window')  
string_roomtype[dataset_test_features['room_type'] < .6] = '3_wall'
string_roomtype[dataset_test_features['room_type'] < .2] = '1_wall'
string_roomtype[dataset_test_features['room_type'] < -.2] = '3_window'
string_roomtype[dataset_test_features['room_type'] < -.6] = '1_window'
dataset_test_features['room_type'] = string_roomtype

# v_ar to discrete
string_v_ar = dataset_test_features['v_ar'].apply(lambda x: .5)  
string_v_ar[dataset_test_features['v_ar'] < .5] = 0
string_v_ar[dataset_test_features['v_ar'] < 0] = -.5
string_v_ar[dataset_test_features['v_ar'] < -.5] = -1
dataset_test_features['v_ar'] = string_v_ar

# Check features' histograms.

_ = dataset_features.hist(bins=20, figsize=(18, 12), xlabelsize=10)

# Double-check that we've done the right thing.
print("Training examples summary:")
display.display(dataset_features.describe())
print("Validation examples summary:")
display.display(dataset_validation_features.describe())

print("Training targets summary:")
display.display(dataset_targets.describe())
print("Validation targets summary:")
display.display(dataset_validation_targets.describe())


print("Test examples summary:")
display.display(dataset_test_features.describe())
print("Validation targets summary:")
display.display(dataset_test_targets.describe())

"""## 5. Treinando a RNA
### _5. Training ANN_
"""

def construct_feature_columns():
  """Construct the TensorFlow Feature Columns.

  Returns:
    A set of feature columns
  """ 
  
  area = tf.feature_column.numeric_column("area")
  azimuth = tf.feature_column.numeric_column("azimuth")
  floor_height = tf.feature_column.numeric_column("floor_height")
  absorptance = tf.feature_column.numeric_column("absorptance")
  shading = tf.feature_column.numeric_column("shading")
  wall_u = tf.feature_column.numeric_column("wall_u")
#   wall_ct = tf.feature_column.numeric_column("wall_ct")
  wwr = tf.feature_column.numeric_column("wwr")
  glass = tf.feature_column.numeric_column("glass")
  open_fac = tf.feature_column.numeric_column("open_fac")
  people = tf.feature_column.numeric_column("people")
  ground = tf.feature_column.numeric_column("ground")
  roof = tf.feature_column.numeric_column("roof")
  v_ar = tf.feature_column.numeric_column("v_ar")
  
  terms = ('0_window', '3_wall', '1_wall', '3_window', '1_window')
  room_type = tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list(key="room_type", vocabulary_list=terms))

  return set([area,
              azimuth,
              floor_height,
              absorptance,
              shading,
              wall_u,
#               wall_ct,
              wwr,
              glass,
              open_fac,
              people,
              ground,
              roof,
              v_ar,
              room_type
             ])

def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
    """Trains a neural network model.
  
    Args:
      features: pandas DataFrame of features
      targets: pandas DataFrame of targets
      batch_size: Size of batches to be passed to the model
      shuffle: True or False. Whether to shuffle the data.
      num_epochs: Number of epochs for which data should be repeated. None = repeat indefinitely
    Returns:
      Tuple of (features, labels) for next data batch
    """
    
    # Convert pandas data into a dict of np arrays.
    features = {key:np.array(value) for key,value in dict(features).items()}                                           
 
    # Construct a dataset, and configure batching/repeating.
    ds = Dataset.from_tensor_slices((features,targets)) # warning: 2GB limit
    ds = ds.batch(batch_size).repeat(num_epochs)
    
    # Shuffle the data, if specified.
    if shuffle:
      ds = ds.shuffle(10000)
    
    # Return the next batch of data.
    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels

def train_nn_regression_model(
    my_optimizer,
    steps,
    batch_size,
    hidden_units,
    target,
    training_examples,
    training_targets,
    validation_examples,
    validation_targets,
    periods = 10):
  """Trains a neural network regression model.
  
  In addition to training, this function also prints training progress information,
  as well as a plot of the training and validation loss over time.
  
  Args:
    my_optimizer: An instance of `tf.train.Optimizer`, the optimizer to use.
    steps: A non-zero `int`, the total number of training steps. A training step
      consists of a forward and backward pass using a single batch.
    batch_size: A non-zero `int`, the batch size.
    hidden_units: A `list` of int values, specifying the number of neurons in each layer.
    training_examples: A `DataFrame` containing one or more columns from
      the dataset to use as input features for training.
    training_targets: A `DataFrame` containing exactly one column from
      the dataset to use as target for training.
    validation_examples: A `DataFrame` containing one or more columns from
      the dataset to use as input features for validation.
    validation_targets: A `DataFrame` containing exactly one column from
      the dataset to use as target for validation.
      
  Returns:
    A tuple `(estimator, training_losses, validation_losses)`:
      estimator: the trained `DNNRegressor` object.
      training_losses: a `list` containing the training loss values taken during training.
      validation_losses: a `list` containing the validation loss values taken during training.
  """

  steps_per_period = steps / periods
  
  # Create a DNNRegressor object.
  my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
  dnn_regressor = tf.estimator.DNNRegressor(
      feature_columns=construct_feature_columns(),
      hidden_units=hidden_units,
      optimizer=my_optimizer,
      model_dir='ann'
  )
  
  # Create input functions.
  training_input_fn = lambda: my_input_fn(training_examples, 
                                          training_targets[target], 
                                          batch_size=batch_size)
  predict_training_input_fn = lambda: my_input_fn(training_examples, 
                                                  training_targets[target], 
                                                  num_epochs=1, 
                                                  shuffle=False)
  predict_validation_input_fn = lambda: my_input_fn(validation_examples, 
                                                    validation_targets[target], 
                                                    num_epochs=1, 
                                                    shuffle=False)

  # Train the model, but do so inside a loop so that we can periodically assess
  # loss metrics.
  print("Training model...")
  print("RMSE (on training data):")
  training_rmse = []
  validation_rmse = []
  for period in range (0, periods):
    # Train the model, starting from the prior state.
    dnn_regressor.train(
        input_fn=training_input_fn,
        steps=steps_per_period
    )
    # Take a break and compute predictions.
    training_predictions = dnn_regressor.predict(input_fn=predict_training_input_fn)
    training_predictions = np.array([item['predictions'][0] for item in training_predictions])
    
    validation_predictions = dnn_regressor.predict(input_fn=predict_validation_input_fn)
    validation_predictions = np.array([item['predictions'][0] for item in validation_predictions])
    
    # Compute training and validation loss.
    training_root_mean_squared_error = math.sqrt(
        metrics.mean_squared_error(training_predictions, training_targets))
    validation_root_mean_squared_error = math.sqrt(
        metrics.mean_squared_error(validation_predictions, validation_targets))
    # Occasionally print the current loss.
    print("  period %02d : %0.4f" % (period, training_root_mean_squared_error))
    # Add the loss metrics from this period to our list.
    training_rmse.append(training_root_mean_squared_error)
    validation_rmse.append(validation_root_mean_squared_error)
  print("Model training finished.")

  # Output a graph of loss metrics over periods.
  plt.ylabel("RMSE")
  plt.xlabel("Periods")
  plt.title("Root Mean Squared Error vs. Periods")
  plt.tight_layout()
  plt.plot(training_rmse, label="training")
  plt.plot(validation_rmse, label="validation")
  plt.legend()

  print("Final RMSE (on training data):   %0.4f" % training_root_mean_squared_error)
  print("Final RMSE (on validation data): %0.4f" % validation_root_mean_squared_error)

  return dnn_regressor

EHF = train_nn_regression_model(
    my_optimizer=tf.train.AdagradOptimizer(learning_rate=0.05), # AdagradOptimizer
    steps=150000,
    batch_size=50,
    hidden_units=[50, 20], # duas camadas
    target=target,
    training_examples=dataset_features,
    training_targets=dataset_targets,
    validation_examples=dataset_validation_features,
    validation_targets=dataset_validation_targets)

"""## 6. Avaliar desempenho
### _6. Evaluate performance_
"""

predict_validation_input_fn = lambda: my_input_fn(dataset_validation_features, 
                                                  dataset_validation_targets[target], 
                                                  num_epochs=1, 
                                                  shuffle=False)

validation_predictions = EHF.predict(input_fn=predict_validation_input_fn)
validation_predictions = np.array([item['predictions'][0] for item in validation_predictions])

d = {'pred': validation_predictions, 'simulado': dataset_validation_targets[target]}
plot_df = pd.DataFrame(data = d)
plt.plot([0,max(plot_df['pred'].max(),plot_df['simulado'].max())],[0,max(plot_df['pred'].max(),plot_df['simulado'].max())])
plt.scatter(plot_df['pred'], plot_df['simulado'], alpha = .03)

filename_validation = 'ann_validation_'+datetime.today().strftime('%m-%d')+'.csv'
plot_df.to_csv(filename_validation)

predict_test_input_fn = lambda: my_input_fn(dataset_test_features, 
                                                  dataset_test_targets[target], 
                                                  num_epochs=1, 
                                                  shuffle=False)

test_predictions = EHF.predict(input_fn=predict_test_input_fn)
test_predictions = np.array([item['predictions'][0] for item in test_predictions])

d = {'pred': test_predictions, 'simulado': dataset_test_targets[target]}
plot_df = pd.DataFrame(data = d)

plt.plot([0,max(plot_df['pred'].max(),plot_df['simulado'].max())],[0,max(plot_df['pred'].max(),plot_df['simulado'].max())])
plt.scatter(plot_df['pred'], plot_df['simulado'], alpha = .03)

filename_test = 'ann_test_'+datetime.today().strftime('%m-%d')+'.csv'
plot_df.to_csv(filename_test)

"""## Salvar e carregar a RNA
### _Save and load ANN_
"""

from google.colab import files

"""### Save validation and test results"""

files.download(filename_validation)

files.download(filename_test)

"""### Zip ANN"""

!zip -r /content/ann.zip /content/ann

"""### Load ANN"""

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

!unzip ann.zip 
!mv content/ann .

EHF = tf.estimator.DNNRegressor(
      feature_columns=construct_feature_columns(),
      hidden_units=[50,20],
      model_dir='ann'
      )