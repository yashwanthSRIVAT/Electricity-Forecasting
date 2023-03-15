from sklearn.model_selection import train_test_split
import pandas as pd
from django.conf import settings
import os
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
import numpy as np
import matplotlib.pyplot as plt

dataset = os.path.join(settings.MEDIA_ROOT, 'Shanghai_data.csv')
df = pd.read_csv(dataset)
df = df.drop(['date'], axis=1)
df['nextDay'] = df.mean(numeric_only=True, axis=1)

X = df.iloc[:,:-1].values # indipendent variable
y = df.iloc[:,-1].values # Dependent variable

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3,random_state=0)

def calc_rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


def simple_linear_regression():
    print("-----------------Simple Linear------------------")
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    # Predicting the Test set results
    y_pred = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print('Meas Absolute Error:', mae)
    mse = mean_squared_error(y_test, y_pred)
    print('Mean Squared Error:', mse)
    r2score = r2_score(y_test, y_pred)
    print('R2-Score :', r2score)
    rmse = calc_rmse(y_test, y_pred)
    print('RMSE:', rmse)



def lasso_regression():
    print("-----------------Lasso Linear------------------")
    regressor = Lasso()
    regressor.fit(X_train, y_train)
    # import pickle
    # file = 'model.alex'
    # pickle.dump(regressor, open(file,'wb'))
    # Predicting the Test set results
    y_pred = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print('Meas Absolute Error:', mae)
    mse = mean_squared_error(y_test, y_pred)
    print('Mean Squared Error:', mse)
    r2score = r2_score(y_test, y_pred)
    print('R2-Score :', r2score)
    rmse = calc_rmse(y_test, y_pred)
    print('RMSE:', rmse)
    mae= mean_absolute_percentage_error(y_test,y_pred)
    return mae,mse


def kernel_my_lasso():
    # regressor = KernelRidge(alpha=0.1,kernel='rbf', degree=4)
    regressor = Lasso(alpha=0.1,max_iter=1000)
    regressor.fit(X_train, y_train)
    # Predicting the Test set results
    y_pred = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print('Meas Absolute Error:', mae)
    mse = mean_squared_error(y_test, y_pred)
    print('Mean Squared Error:', mse)
    r2score = r2_score(y_test, y_pred)
    print('R2-Score :', r2score)
    rmse = calc_rmse(y_test, y_pred)
    print('RMSE:', rmse)
    mae = mean_absolute_percentage_error(y_test, y_pred)
    # visualizing the Test set results
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.plot(y_test, color="red", label="Original")
    ax.plot(y_pred, color="green", label="Predections")
    # ax.plot(dir_fcast, color="green", label="Direct forecast")
    ax.set_title(f"Original vs predection")
    ax.legend()
    # plt.show()

    return mae,mse

