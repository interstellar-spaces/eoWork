import pandas as pd

# import raw data from full excel
raw_data = pd.read_csv(r"C:\Users\dnguy\Downloads\transaction_dec.csv")
# change data column to no-space, all-lower-case for convenience
raw_data.columns = raw_data.columns.str.strip().str.lower().str.replace(' ','_')
# select only necessary columns
data = raw_data[["date","user_name", "membership_used","total_amount","refund_amount","payment_type"]]

# generate the net_sum revenue, including Koloni commissino
def rev(data):
    if data["total_amount"] == 0:
        return 0
    elif data["total_amount"] != 0 and data["payment_type"] == "Offline":
        return 0
    elif data["total_amount"] != 0 and data["payment_type"] == "Online":
        if pd.isna(data["refund_amount"]):
            rev = data["total_amount"]
        else:
            rev = data["total_amount"] - data["refund_amount"]
        return rev
    else:
        return 0
data["rev"] = data.apply(rev, axis = 'columns')

# Generate pure revenue, solely for eo
commission_lumpsum = 0.5
commission_time = 0.05
def net_rev (data):
    if data["rev"] > 0 and data["membership_used"] == "YES":
        net_rev = data["rev"] * (1 - commission_time)
    elif data["rev"] > 0 and data["membership_used"] != "YES":
        net_rev = (data["rev"] - commission_lumpsum) * (1 - commission_time)
    else:
        return 0
    return net_rev
data["net_revenue"] = data.apply(net_rev, axis = 'columns')

ppr_revenue = data["net_revenue"].sum()
# earlybird_members = float(input("# of early birds = "))
# normal_members = float(input("# of normal members = "))
# procrastinators = float(input ("# of procrastinator members = "))
earlybird_members = 51
normal_members = 89
procrastinators = 17
membership_revenue = 0.95 * (25*earlybird_members +
                             30 * normal_members +
                             18 * procrastinators)

total_revenue = membership_revenue + ppr_revenue


############################################################
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np

# Categorically analyze date-by-date data
data['date'] = pd.to_datetime(data['date'])
data['accurate_to_date'] = pd.to_datetime(data['date']).dt.to_period('D')
# Create pivot table for daily revenue
daily = data.pivot_table(values = 'net_revenue',
                         index = 'accurate_to_date',
                         aggfunc = np.sum)
daily["date"] = daily.index

# add in cumulative revenue
def cumulate(data, column):
    cumulated = 0
    cumulate_list = []
    for transaction in data[column]:
        cumulated = cumulated + transaction
        cumulate_list.append(cumulated)
    return cumulate_list
cumulate_list = cumulate(daily,"net_revenue")
daily["cumulated_revenue"] = cumulate_list

# Create pivot table about ridership
daily_ride = data.pivot_table(values = 'user_name',
                              index = 'accurate_to_date',
                              aggfunc = 'count')
daily_ride["date"] = daily_ride.index
daily_ride.rename(columns = {'user_name':'rides'}, inplace = True)
cumulate_rides_list = cumulate(daily_ride,'rides')
daily_ride["cumulated_rides"] = cumulate_rides_list

# plotting revenue data
fig, axs = plt.subplots(2,2, sharex = True, gridspec_kw = {'hspace': 0})
axs[0,0].set_title('revenue data')
daily.plot(kind = 'line', x = 'date', y = 'net_revenue',
               alpha = 1, color = "#F8B195", marker = '.', linewidth = 2,
               ax = axs[0,0])
daily.plot(kind = 'line', x = 'date', y = 'cumulated_revenue',
               alpha = 1, color = '#99B898', linewidth = 4,
               ax = axs[1,0])
axs[1,0].fill_between(daily["date"].tolist(), cumulate_list, 
                      alpha = 0.5, color = '#99B898')
# plotting ridership data
axs[0,1].set_title('ridership data')
daily_ride.plot(kind = 'line', x = 'date', y = 'rides',
               alpha = 1, color = "#E84A5F", marker = '.', linewidth = 2,
               ax = axs[0,1])
daily_ride.plot(kind = 'line', x = 'date', y = 'cumulated_rides',
               alpha = 1, color = '#45ADA8', linewidth = 4,
               ax = axs[1,1])
axs[1,1].fill_between(daily["date"].tolist(), cumulate_rides_list, 
                      alpha = 0.5, color = '#45ADA8')


print("------------------ net revenue ----------------")
print("PPR Revenue = $%.2f" % ppr_revenue)
print("Membership Revenue = $%.2f" % membership_revenue)
print("Total Revenue = $%.2f" % total_revenue)
print("-----------------------------------------------")

plt.show()
