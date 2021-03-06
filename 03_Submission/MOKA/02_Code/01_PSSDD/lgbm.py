#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:10:44 2017

@author: lukaskemmer
"""
from load_data import *
from data_visualization import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import feature_selection, decomposition
<<<<<<< HEAD
from sklearn.model_selection import StratifiedKFold, train_test_split
from lightgbm import LGBMClassifier
from functions import *
from feature_engineering import *

=======
from sklearn.model_selection import KFold
from sklearn.ensemble import ExtraTreesClassifier
from lightgbm import LGBMClassifier
from functions import *
from feature_engineering import *
from sklearn.preprocessing import OneHotEncoder
>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498

## ============================ 0. Set parameters ========================== ##

# Define parameters
<<<<<<< HEAD
load_new_data = True # Set True to reload and format data
subset_data = False # Set Treu to select a random subsample of X, Y for testing
subset_size = 10000 # Set the size of the random subsample
train_model = True # Set True if model should be trained
make_predictions = False # Set true if prediction for submission should be made
k = 5 # Number of folds for cross-validation
np.random.seed(0) # Random seed to produce comparable results

# Set model parameters for LGBM
lgb_params = {}
lgb_params['learning_rate'] = 0.015
lgb_params['n_estimators'] = 650
lgb_params['max_bin'] = 10 # dataset
lgb_params['subsample'] = 0.8
lgb_params['subsample_freq'] = 10  
lgb_params['min_child_samples'] = 500
lgb_params['feature_fraction'] = 0.9 # somewhere else
lgb_params['bagging_freq'] = 1 # Somewhere else
lgb_params['random_state'] = 200
lgb_params['max_depth'] = 6
=======
load_new_data = True  # Set True to reload and format data
subset_data = False  # Set Treu to select a random subsample of X, Y for testing
subset_size = 50000  # Set the size of the random subsample
train_model = True  # Set True if model should be trained
make_predictions = True  # Set true if prediction for submission should be made
k = 5  # Number of folds for cross-validation
np.random.seed(0)  # Random seed to produce comparable results

# Set model parameters for LGBM
lgb_params = {}
lgb_params['n_estimators'] = 1100
lgb_params['max_depth'] = 4
lgb_params['learning_rate'] = 0.02
lgb_params['feature_fraction'] = 0.9
lgb_params['bagging_freq'] = 1
lgb_params['random_state'] = 0  # Define features to be used

train_features = ["ps_car_13",
                  "ps_reg_03",
                  "ps_ind_03",
                  "ps_ind_15",
                  "ps_reg_02",
                  "ps_car_14",
                  "ps_car_12",
                  "ps_reg_01",
                  "ps_car_15",
                  "ps_ind_01",
                  "ps_car_11",
                  # "ps_calc_09", # Maybe drop
                  # "ps_calc_05", # Maybe drop
                  "ps_ind_14",
                  "ps_ind_17_bin",
                  "ps_ind_08_bin",
                  "ps_ind_09_bin",
                  "ps_ind_18_bin",
                  "ps_ind_12_bin",
                  "ps_ind_16_bin",
                  "ps_ind_07_bin",
                  "ps_ind_06_bin",
                  "ps_ind_05_cat",
                  "ps_car_01_cat",
                  "ps_car_07_cat",
                  "ps_car_03_cat",
                  "ps_car_06_cat",
                  "ps_car_04_cat",
                  "ps_car_09_cat",
                  "ps_car_02_cat",
                  "ps_ind_02_cat",
                  "ps_car_05_cat",
                  "ps_car_08_cat",
                  "ps_ind_04_cat",
                  "ps_car_11_cat"]
>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498

## ======================= 1. Load and visualize data ====================== ##
print("\n1. Loading and visualizing data ...\n")
if load_new_data:
    # Load raw data
    X_train_raw, y_train_raw, X_test_raw, X_test_ids, X_train_ids, column_names = read_data()
<<<<<<< HEAD
    
=======

>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498
    # Format data
    X_train_formatted, X_test_formatted = format_data(X_train_raw.copy(),
                                                      X_test_raw.copy(),
                                                      column_names)

    # Describe data
    X_train_summary, X_test_summary, X_train_freq, X_test_freq, X_train_missing, X_test_missing = describe_data(
        X_train_formatted, X_test_formatted)

# Copy formatted data
X_train = X_train_formatted.copy()
y_train = y_train_raw.copy()
X_test = X_test_formatted.copy()

# Randomly subset the data for faster computation during train/test
if subset_data:
    X_train = X_train.sample(n=subset_size, replace=False,
                             random_state=0).reset_index(drop=True)
    y_train = y_train.sample(n=subset_size, replace=False,
                             random_state=0).reset_index(drop=True)

# Plot distributions of features for training and testing data
visualize_features(X_train, "Training data", bin_features=False,
                   cat_features=0, cont_features=False)
visualize_features(X_test, "Testing data", bin_features=False,
                   cat_features=0, cont_features=False)

## ========================= 2. Feature engineering ======================== ##
print("\n2. Adding and selecting features ...\n")
# Select features
train_features = [col for col in X_train_raw.columns if not "_calc_" in col]
X_train = X_train[train_features]
X_test = X_test[train_features]

<<<<<<< HEAD
# Don't Replace NAs for LGBM
print("\n   a) Don't replace NAs for LGBM ...\n")
#X_train, X_test = replace_nas(X_train, X_test)

# Add combinations of features
print("\n   a) Add feature combinations ...\n")
# Create list with features that should be combined  
combinations = [('ps_reg_01', 'ps_car_02_cat'),
                ('ps_reg_01', 'ps_car_04_cat')]

=======
# Add combinations of features
print("\n   a) Add feature combinations ...\n")
# Create list with features that should be combined
combinations = [('ps_reg_01', 'ps_car_02_cat'), ('ps_reg_01', 'ps_car_04_cat')]
>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498
# Add combinations
X_train, X_test = add_combination_features(X_train, X_test, combinations)

# Encode categorical data
print("\n   b) Add encoded categorical features ...\n")
for col in [col for col in X_train.columns if '_cat' in col]:
    X_train[col + "_avg"], X_test[col + "_avg"] = target_encode(
<<<<<<< HEAD
            trn_series=X_train[col],
            tst_series=X_test[col],
            target=y_train,
            min_samples_leaf=200,
            smoothing=10) 

# Feature engineering
print("\n   b) Add features ...\n")    
=======
        trn_series=X_train[col],
        tst_series=X_test[col],
        target=y_train,
        min_samples_leaf=200,
        smoothing=10)

# Create dummies for categorical features
print("\n   c) Add dummies for categorical features ...\n")
# Create list with columns for which dummies should be created
>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498
col_names = ["ps_car_07_cat",
             "ps_car_03_cat",
             "ps_car_09_cat",
             "ps_car_02_cat",
             "ps_ind_02_cat",
             "ps_car_05_cat"]
<<<<<<< HEAD
X_train, X_test = create_dummies(X_train, X_test, col_names)

# Recursive feature elimination
print("\n   b) Recursive feature elimination ...\n")
'''
num_feat = 50
while X_train.shape[0]>num_feat:
    print(X_train.shape[0])
    print(X_train.shape[0]>num_feat)
    X_train, X_validate, y_train, y_validate = train_test_split(X_train, Y_train, 
                                                                test_size=0.2, random_state=0)
    # train model
    model = LGBMClassifier(**lgb_params)
    model = model.fit(X_train, y_train)
    # Find feature with least importance
    column_to_delete = X_train.columns[np.argmin(model.feature_importances_)]
    print("Current gini coefficient: %f" %(test_model(model, X_validate, y_validate)))
    print("Drop feature: " + column_to_delete)
    print("%d features remaining" % (len(X_train.columns)))
    # Drop least important feature
    X_train.drop(column_to_delete, axis=1, inplace=True)
    X_test.drop(column_to_delete, axis=1, inplace=True)
'''
train_features = recursive_feature_elimination(X_train.copy(), y_train.copy(), LGBMClassifier(**lgb_params), 40) # use 53
X_train = X_train[train_features]
X_test = X_test[train_features]
## ===================== 3. Model training and evaluation ================== ##    
=======
# Add dummie features
X_train, X_test = create_dummies(X_train, X_test, col_names)

## ===================== 3. Model training and evaluation ================== ##
>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498
print("\n3. Training and validating model\n")
# Split data into first-stage training set and second stage validation set
X_train["id"] = X_train_ids
X_train, X_validation_2, y_train, y_validation_2 = train_test_split(
    X_train, y_train, test_size=0.2, random_state=0)

# Reset indexes for cross-validation
X_train = X_train.reset_index(drop=True).drop('id', axis=1)
y_train = y_train.reset_index(drop=True)

if train_model:
    # Initialize model
    lgbm = LGBMClassifier(**lgb_params)

    # Create cross validation iterator
<<<<<<< HEAD
    kf = StratifiedKFold(n_splits=k, random_state=1, shuffle=True)
    
=======
    kf = KFold(n_splits=k, random_state=1, shuffle=True)

>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498
    # Initialize array for evaluation results
    normalized_gini = []

    # Make copies for X, Y to b e used within CV
    X = X_train.copy()
    y = y_train.copy()
    y_pred = np.zeros(X_test.shape[0])
    y_pred_validation = np.zeros(X_validation_2.shape[0])

    for train_index, validation_index in kf.split(X, y):
        print("Cross-validation, Fold %d" % (len(normalized_gini) + 1))

        # Split data into training and testing set
        X_train = X.iloc[train_index, :].copy()
        X_validate = X.iloc[validation_index, :].copy()
        y_train = y[train_index]
        y_validate = y[validation_index]

        lgbm = lgbm.fit(X_train, y_train)

        # Test the model
        normalized_gini.append(test_model(lgbm, X_validate, y_validate))

        # Make test set prediction
<<<<<<< HEAD
        y_pred += lgbm.predict_proba(X_test[X_train.columns])[:,1]
        
        del X_train, X_validate, y_train, y_validate

    # Evaluate results from CV
    print("Normalized gini coefficient %f +/- %f" % (np.mean(normalized_gini), 
                                                     2*np.std(normalized_gini)))
    
    # Calculate prediction
    y_pred /= k
=======
        y_pred += lgbm.predict_proba(X_test[X_train.columns])[:, 1]

        # Make predictions for the second stage training set
        y_pred_validation += lgbm.predict_proba(X_validation_2[X_train.columns])[:, 1]

        del X_train, X_validate, y_train, y_validate

        # Evaluate results from CV
    print("Normalized gini coefficient %f +/- %f" % (np.mean(normalized_gini),
                                                     2 * np.std(normalized_gini)))
>>>>>>> 72aa6c47feff25b94814ab9aac52993afeda3498

    # Calculate prediction as average of fold-prediction
    y_pred /= k
    y_pred_validation /= k

## =========================== 4. Output results =========================== ##
if True:
    # Create dataframes for second stage model
    second_stage_train_test = pd.DataFrame(
        {'id': X_validation_2.id, 'lgbm_pred': y_pred_validation, 'target': y_validation_2})

    # Output results
    second_stage_train_test.to_csv('../03_Results/lgbm_2_stage_train_test.csv', sep=',', index=False)

if make_predictions:
    print("\n4. Saving results\n")

    # Create output dataframes
    submission = pd.DataFrame({'id': X_test_ids, 'target': y_pred})

    # Output results
    submission.to_csv('../03_Results/lgbm_prediction.csv', sep=',', index=False)
