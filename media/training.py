# imports
import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
from django.conf import settings
import os
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.kernel_approximation import RBFSampler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Processed_data.csv')
df.drop(0)

# Splitting the dataset into features (X) and target (y)
X = df.iloc[:, :-1].values  # First 7 columns as features
y = df.iloc[:, -1].values   # Last column as target

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)


def kernel_my_lasso():
    print("-----------------Kernel Lasso Regression------------------")

    # Transform the data using the RBF kernel
    transformer = RBFSampler(n_components=100, random_state=42)
    X_train_transformed = transformer.fit_transform(X_train)
    X_test_transformed = transformer.transform(X_test)

    # Perform Lasso regression on the transformed data
    regressor = Lasso(alpha=0.1,max_iter=1000)
    regressor.fit(X_train_transformed, y_train)

    # Predicting the Test set results
    y_pred = regressor.predict(X_test_transformed)

    # Calculating errors
    mse = mean_squared_error(y_test, y_pred)
    print('Mean Squared Error:', mse)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    print('Mean Absoslute Percentage Error:', mse)
    
    # Save the trained model using pickle
    with open('kernel_lasso_model.pkl', 'wb') as f:
        pickle.dump((transformer, regressor), f)

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.plot(y_test, color="red", label="Original")
    ax.plot(y_pred, color="green", label="Predections")
    # ax.plot(dir_fcast, color="green", label="Direct forecast")
    ax.set_title(f"Original vs predection")
    ax.legend()
    # plt.show()

    return mse, mape

kernel_my_lasso()