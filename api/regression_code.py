import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm
from math import sqrt
import random


def run_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y.values, test_size=0.2, random_state=123)

    min_max_scaler = preprocessing.MinMaxScaler()
    X_train_scaled = min_max_scaler.fit_transform(X_train)
    X_test_scaled = min_max_scaler.transform(X_test)

    clfs = {'linearReg': {'model': linear_model.LinearRegression(), 'params': {}},
            # 'RidgeReg': {'model': linear_model.Ridge(), 'params': {'alpha': list(np.arange(0.001, 0.01, 0.001))}},
            # 'LassoReg': {'model': linear_model.Lasso(), 'params': {'alpha': list(np.arange(0.001, 0.01, 0.001))}},
            # 'DTReg': {'model': DecisionTreeRegressor(), 'params': {'max_depth': list(np.arange(1, 10, 1))}},
            # 'rfReg':{'model': RandomForestRegressor(), 'params':{'max_depth': list(np.arange(4, 10, 1)), 'n_estimators':list(np.arange(50,125,25))}},
            # 'knnReg': {'model': KNeighborsRegressor(), 'params': {'n_neighbors': list(np.arange(5, 30, 5))}}}  # ,
            # 'svmReg':{'model': svm.SVR(), 'params':{'C':list(np.arange(0.05,1,0.01))}}}
            }

    # compare classifier
    clf_dict = {'clf': [], 'train_mse': [], 'train_mae': [], 'train_rmse': [], 'test_mse': [], 'test_mae': [], 'test_rmse': [],
                'contain_neg_entries': []}

    df_pred = pd.DataFrame(X_test)
    df_pred.columns = X.columns
    df_pred['y_true'] = y_test

    # compare classifier
    for i, clf in enumerate(clfs):
        params = clfs[clf]['params']
        model = clfs[clf]['model']

        model_cv = GridSearchCV(model, params, cv=5)
        model_cv.fit(X_train_scaled, y_train)
        # print(model_cv.best_params_)
        clf_tuned = model_cv.best_estimator_

        clf_tuned.fit(X_train_scaled, y_train)

        # train errors
        y_pred_train = clf_tuned.predict(X_train_scaled)
        train_mse = np.round(mean_squared_error(y_train, y_pred_train), 3)
        train_mae = np.round(mean_absolute_error(y_train, y_pred_train), 3)
        train_rmse = np.round(np.sqrt(train_mse), 3)

        # test errors
        y_pred_test = clf_tuned.predict(X_test_scaled)
        test_mse = np.round(mean_squared_error(y_test, y_pred_test), 3)
        test_mae = np.round(mean_absolute_error(y_test, y_pred_test), 3)
        test_rmse = np.round(np.sqrt(test_mse), 3)

        neg_entries = y_pred_test[y_pred_test < 0].sum()

        clf_dict['clf'].append(clf)
        clf_dict['train_mse'].append(train_mse)
        clf_dict['train_mae'].append(train_mae)
        clf_dict['train_rmse'].append(train_rmse)
        clf_dict['test_mse'].append(test_mse)
        clf_dict['test_mae'].append(test_mae)
        clf_dict['test_rmse'].append(test_rmse)
        clf_dict['contain_neg_entries'].append(neg_entries)

        df_pred[clf + '_pred'] = y_pred_test

    result = pd.DataFrame(clf_dict)
    # print(pd.DataFrame(clf_dict))

    return result, df_pred
