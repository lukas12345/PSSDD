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
from sklearn import model_selection, feature_selection, decomposition
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
from xgboost import plot_tree
from functions import *
from feature_engineering import *

## ============================ 0. Set parameters ========================== ##

load_new_data = True # Set True to reload and format data
subset_data = False # Set Treue to use only 10000 records for training
train_mode = True # Set True if model should be trained
make_predictions = True # Set true if prediction for submission should be made
k = 5 # Number of folds for cross-validation
na_threshold = 100 # All features with more %NA will be dropped
num_features = 20 # Number of top features that will be used
np.random.seed(123) # Random seed to produce comparable results
## ======================= 1. Load and visualize data ====================== ##
print("\n1. Loading and visualizing data ...\n")
if load_new_data:
    # Load raw data
    X_train_raw, y_train_raw, X_test_raw, X_test_ids, column_names = read_data()
    
    # Format data
    X_train_formatted, X_test_formatted = format_data(X_train_raw.copy(),
                                                      X_test_raw.copy(),
                                                      column_names)
    
    # Describe data
    X_train_summary, X_test_summary, X_train_freq, X_test_freq, X_train_missing, X_test_missing = describe_data(X_train_formatted, X_test_formatted)

# Copy formatted data
X_train = X_train_formatted.copy()
y_train = y_train_raw.copy()
X_test = X_test_formatted.copy()

# Randomly subset the data for faster computation during train/test
if subset_data:
    X_train = X_train.sample(n=100000, replace=False, random_state=0).reset_index(drop=True)
    y_train = y_train.sample(n=100000, replace=False, random_state=0).reset_index(drop=True)

#visualize_features(X_train, y_train, bin_features=True, cat_features=True, 
#                   cont_features=True)

## ========================= 2. Feature engineering ======================== ##
print("\n2. Adding and selecting features ...\n")
'''
# Drop columns that have more than 'na_threshold' % NAs, based on X_train data!
irrelevant_columns = list(X_train_missing[X_train_missing>na_threshold].index)
X_train = X_train.drop(irrelevant_columns, axis=1)
X_test = X_test.drop(irrelevant_columns, axis=1)

# Drop features unrelated to forecast

X_train = X_train.drop(['ps_calc_01', 'ps_calc_02', 'ps_calc_03', 'ps_calc_04', 'ps_calc_05', 'ps_calc_06',
                        'ps_calc_07', 'ps_calc_08', 'ps_calc_09', 'ps_calc_10', 'ps_calc_11', 'ps_calc_12',
                        'ps_calc_13', 'ps_calc_14', 'ps_calc_15_bin', 'ps_calc_16_bin', 'ps_calc_17_bin',
                        'ps_calc_18_bin', 'ps_calc_19_bin', 'ps_calc_20_bin', 'ps_car_10_cat', 'ps_ind_10_bin',
                        'ps_ind_13_bin', 'ps_ind_12_bin'], axis=1)

'''
# Replace NAs
print("\n   a) Replace NAs ...\n")
X_train, X_test = replace_nas(X_train, X_test)

# Feature engineering
print("\n   b) Add features ...\n")    
X_train, X_test = add_features(X_train, X_test)

# Encode categorical data
for col in [col for col in X_train.columns if '_cat' in col]:
    X_train[col + "_avg"], X_test[col + "_avg"] = target_encode(
            trn_series=X_train[col],
            tst_series=X_test[col],
            target=y_train,
            min_samples_leaf=200,
            smoothing=10,
            noise_level=0
            )

# Feature evaluation
print("\n   c) Evaluate features ...\n")
feature_importance = get_feature_importance(
        X_train.copy().select_dtypes(exclude=['category']), 
        y_train, 
        model = XGBClassifier(n_jobs = 8)) 
#ExtraTreesClassifier(n_estimators=250,random_state=0))

# Select X best features
train_features = feature_importance.iloc[:50,0]
additional_features = [
    "ps_car_13",  #            : 1571.65 / shadow  609.23
	"ps_reg_03",  #            : 1408.42 / shadow  511.15
	#"ps_ind_05_cat",  #        : 1387.87 / shadow   84.72
	"ps_ind_03",  #            : 1219.47 / shadow  230.55
	"ps_ind_15",  #            :  922.18 / shadow  242.00
	"ps_reg_02",  #            :  920.65 / shadow  267.50
	"ps_car_14",  #            :  798.48 / shadow  549.58
	"ps_car_12",  #            :  731.93 / shadow  293.62
	#"ps_car_01_cat",  #        :  698.07 / shadow  178.72
	#"ps_car_07_cat",  #        :  694.53 / shadow   36.35
	"ps_ind_17_bin",  #        :  620.77 / shadow   23.15
	#"ps_car_03_cat",  #        :  611.73 / shadow   50.67
	"ps_reg_01",  #            :  598.60 / shadow  178.57
	"ps_car_15",  #            :  593.35 / shadow  226.43
	"ps_ind_01",  #            :  547.32 / shadow  154.58
	"ps_ind_16_bin",  #        :  475.37 / shadow   34.17
	"ps_ind_07_bin",  #        :  435.28 / shadow   28.92
	#"ps_car_06_cat",  #        :  398.02 / shadow  212.43
	#"ps_car_04_cat",  #        :  376.87 / shadow   76.98
	"ps_ind_06_bin",  #        :  370.97 / shadow   36.13
	#"ps_car_09_cat",  #        :  214.12 / shadow   81.38
	#"ps_car_02_cat",  #        :  203.03 / shadow   26.67
	#"ps_ind_02_cat",  #        :  189.47 / shadow   65.68
	"ps_car_11",  #            :  173.28 / shadow   76.45
	#"ps_car_05_cat",  #        :  172.75 / shadow   62.92
	"ps_calc_09",  #           :  169.13 / shadow  129.72
	"ps_calc_05",  #           :  148.83 / shadow  120.68
	"ps_ind_08_bin",  #        :  140.73 / shadow   27.63
	#"ps_car_08_cat",  #        :  120.87 / shadow   28.82
	"ps_ind_09_bin",  #        :  113.92 / shadow   27.05
	#"ps_ind_04_cat",  #        :  107.27 / shadow   37.43
	"ps_ind_18_bin",  #        :   77.42 / shadow   25.97
	"ps_ind_12_bin",  #        :   39.67 / shadow   15.52
	"ps_ind_14",  #            :   37.37 / shadow   16.65
    #"ps_car_11_cat"
    ]
train_features = np.unique(np.append(train_features, additional_features))#X_train.select_dtypes(include=['category']).columns))

X_train = X_train[train_features]
X_test = X_test[train_features]

## ===================== 3. Model training and evaluation ================== ##    
print("\n3. Training and validating model\n")
# Select a model
#model = tree.DecisionTreeClassifier() # Decision tree
#model = ensemble.RandomForestClassifier(n_estimators=100) # Random forest
#model = linear_model.LogisticRegression() # Logistic regression
#model = naive_bayes.GaussianNB(priors = [1-np.mean(X_train_raw.target), 
#                                        np.mean(X_train_raw.target)])
xgb = XGBClassifier(max_depth=4, # Maximum tree depth for base learners
                      learning_rate=0.07, # Boosting learning rate (xgb’s “eta”)
                      n_estimators = 400, # Number of boosted trees to fit
                      silent = True, # Whether to print messages while running boosting
                      objective='binary:logistic', # learning objective
                      #booster='gbtree', # Which booster to use: gbtree, gblinear or dart
                      n_jobs = 8, # Number of parallel threads
                      gamma=10, # Minimum loss reduction required to make a further partition on a leaf node of the tree
                      min_child_weight=6, # Minimum sum of instance weight(hessian) needed in a child
                      #max_delta_step=0, # Maximum delta step we allow each tree’s weight estimation to be
                      subsample=.8, # Subsample ratio of the training instance
                      colsample_bytree=.8, # Subsample ratio of columns when constructing each tree
                      #colsample_bylevel=1, # Subsample ratio of columns for each split, in each level
                      reg_alpha=8, # L1 regularization term on weights
                      reg_lambda=1.3, # L2 regularization term on weights
                      scale_pos_weight=1.6) # Balancing of positive and negative weights
                      #base_score=0.5) # The initial prediction score of all instances, global bias

#log = linear_model.LogisticRegression(class_weight='balanced')

if train_mode:    
    # Create cross validation iterator
    kf = model_selection.KFold(n_splits=k, random_state=1, shuffle=True)
    
    # Initialize array for evaluation results
    normalized_gini = []
    
    # Make copies for X, Y to b e used within CV
    X = X_train.copy()
    y = y_train.copy()
    y_pred = np.zeros(X_test.shape[0])
    
    for train_index, validation_index in kf.split(X):
        print("Cross-validation, Fold %d" % (len(normalized_gini)+1))
        
        # Split data into training and testing set
        X_train = X.iloc[train_index,:].copy()
        X_validate = X.iloc[validation_index,:].copy()
        y_train = y[train_index]
        y_validate = y[validation_index]
        
        # Identify categorical columns 
        #cat_cols = [col for col in X_train.columns if '_cat' in col]
        
        # Train the model
        xgb = xgb.fit(X_train, y_train)
        
        # Test the model
        normalized_gini.append(test_model(xgb, X_validate, y_validate))

        # Make test set prediction
        y_pred += xgb.predict_proba(X_test[X_train.columns])[:,1]
        
        del X_train, X_validate, y_train, y_validate

    # Evaluate results from CV
    print("Normalized gini coefficient %f +/- %f" % (np.mean(normalized_gini), 
                                                     2*np.std(normalized_gini)))
    
    # Plot single tree
    plot_tree(xgb)
    plt.show()
    
    # Calculate prediction
    y_pred /= 2*k

## =========================== 4. Output results =========================== ##
print("\n4. Saving results\n")
if make_predictions:
    # Create output dataframe
    results = pd.DataFrame({'id':X_test_ids, 'target':y_pred})
    
    # Output results
    results.to_csv('../03_Results/xgb_prediction.csv', sep=',', index=False)

