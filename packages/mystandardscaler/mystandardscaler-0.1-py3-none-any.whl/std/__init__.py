from sklearn.preprocessing import StandardScaler
import pandas as pd
class pystd:
    def std(x):
        scaler = StandardScaler()
        scaler.fit_transform(x)
        return scaler
    def myshape(x):
        return x.shape