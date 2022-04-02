# importing important modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import numpy as np
import seaborn as sns
from sklearn import linear_model
import statsmodels.api as sm
import datetime
from dateutil.parser import parse
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression


# importing the data as a pandas dataframe
d=pd.read_csv(r'C:\Users\dnguy\OneDrive\Desktop\eo_big_data.csv',
                  date_parser=[1]) #parse the date column into datetime
w=pd.read_csv(r'C:\Users\dnguy\OneDrive\Desktop\new_eo_data.csv',
              date_parser=[1])

# reformat the column names as lowercase with underscores, no spaces
d.columns=d.columns.str.strip().str.lower().str.replace(' ','_')
w.columns=w.columns.str.strip().str.lower().str.replace(' ','_')

# select necessary columns and convert into a pd dataframe
frame=pd.DataFrame(d, columns=["date", "user_name", "total_net_amount", "payment_type",
             "pickup_location", "drop_location"])
actual_data=pd.DataFrame(w, columns=["date", "temperature", "wind", "precipitation", "daily_riders"])

# narrow down time to hours and separate into time column
time=[]
for x in range(0, len(frame.date)):
    dt = parse(frame.date[x])
    time.append(dt.time())
frame['time']=time

# separate date and time into separate columns
frame['date'] = pd.to_datetime(frame.date).dt.to_period('D')

# remove admin users
admin_users = ["James Jia", "Drake Weissman", "Matthew Schneller", "Dan Hu", "Rory Nguyen", "Ella Boscoe"]
for i in range(0, len(admin_users)):
    frame=frame[frame.user_name != admin_users[i]]

# ----------------------------------------------------------------------------------------

# import pickup and drop location data
new=pd.read_excel(r'C:\Users\dnguy\OneDrive\Desktop\new_eo_data.xlsx')



pick=frame.groupby(by=['pickup_location'],
                  axis=0,
                  as_index=True)
pick_agg=pick.agg({'time': 'count'})

hourly= frame.pivot_table(values = 'total_net_amount',
                         index = 'time',
                         aggfunc = ['count', 'sum'])
hourly.reset_index().rename(columns={'count': 'riders', 'sum': 'revenue_total'})

daily=frame.pivot_table(values='total_net_amount',
                        index='date',
                        aggfunc = ['count', 'sum'])
daily.reset_index().rename(columns={'count': 'riders', 'sum': 'revenue_total'})
#daily.to_excel('output.xlsx')

pickup = frame.pivot_table(values = 'time',
                           index = 'pickup_location',
                           aggfunc='max')

#x=hourly.index
#y=np.reshape(hourly.count, (1215,1))
##plt.style.use('seaborn')
#plt.plot_date(x,y)

heat_map=sns.heatmap(pickup)
plt.show()

#fig, ax = plt.subplots()
#x=hourly['count']
#y=hourly['time']
#plt.plot(x,y, 'ro')
#plt.show()

## plotting ridership data
#fig, axs = plt.subplots(2,2, sharex = 'all', gridspec_kw = {'hspace': 0})
#axs[0,1].set_title('ridership data')
#daily.plot(kind = 'line', x = 'date', y = 'riders',
#               alpha = 1, color = "#E84A5F", marker = '.', linewidth = 2)

## create linear regression object
#regr=linear_model.LinearRegression()
## initialize x and y variables

#regr=regr.fit(x,y)
#regr.score
## The coefficients
#print('Coefficients: \n', regr.coef_)
## The r-squared coefficient of determination
#print('Score: %.2f',
#      regr.score)


