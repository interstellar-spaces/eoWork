import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

d=pd.read_excel(r'C:\Users\dnguy\OneDrive\Desktop\drop_time.xlsx')
p=pd.read_excel(r'C:\Users\dnguy\OneDrive\Desktop\pickup_time.xlsx')

d.columns=d.columns.str.strip().str.lower()
p.columns=p.columns.str.strip().str.lower()

drop=pd.DataFrame(d, columns=['time', 'drop', 'count'])
pickup=pd.DataFrame(p, columns=['time', 'pickup', 'count'])
drop.dropna()
pickup.dropna()

drop_time=sns.heatmap(drop)
pickup_time=sns.heatmap(pickup)

plt.show()