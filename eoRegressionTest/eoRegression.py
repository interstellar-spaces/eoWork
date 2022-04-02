# importing important modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import linear_model
import statsmodels.api as sm


# importing the data as a pandas dataframe
frame=pd.read_csv(r'C:\Users\dnguy\OneDrive\Desktop\eo_big_data.csv',
                  date_parser=[1])

df=pd.DataFrame(frame.data, columns=frame.feature_names)
target=pd.DataFrame(frame.target, columns=["total_net_amount"])

x=df["pickup_location"]
y=target["total_net_amount"]

model=sm.OLS(y,x).fit()
predictions=model.predict(x)

model.summary()


