# importing packages and creating session object
import requests
from lxml import html 
import pandas as pd
session_requests=requests.session()

# define dictionary
payload= {"email": "dungnguyen2023@u.northwestern.edu",
          "password": "Northwestern19!"}
login_url="https://kolonishare.com/app/partner/login"
result=session_requests.get(login_url)
tree = html.fromstring(result.text)

# make a login request
result=session_requests.post(
    login_url,
    data=payload,
    headers=dict(referer=login_url))

gps=[]
coord_data=[]
# go to every order's transaction history and find the GPS data by cycling through the order number for bike 399
for ii in range(12684,13220):
    location_url="https://kolonishare.com/app/partner/bike_management/track_location/399/{}".format(ii)
    #print(location_url)
    result=session_requests.get(location_url, headers=dict(referer=location_url))
    tree=html.fromstring(result.content)
    if tree.xpath("//td[@class='text-center']/text")=="No records found":
        break 
    else: 
        gps_data=tree.xpath("//text()")
        for x in range(0,len(gps_data)):
            entry=gps_data[x]
            #new_entry=entry.split("=")[3].split(",")
            gps.append(entry)
    #coord_data.append(gps)
    #gps=[]

#coordinate=pd.DataFrame(gps, columns=['latitude', 'longitude'])
coordinate=pd.DataFrame(gps)
#print(coordinate)
coordinate.to_csv('coord_data_test.csv')




