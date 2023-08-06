import numpy as np

def compute_rmse(y_pred, y_test):
    return ((y_pred - y_test) ** 2).mean() ** 0.5
