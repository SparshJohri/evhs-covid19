import pandas as pd
import numpy as np
import os
import addfips
import requests
import json
import sys
from time import sleep

    
#getting the initial data
file = "../covid-19-data/us-counties.csv"
data1 = pd.read_csv(file)


#filtering out the counties I don't want to look at
minimum_deaths_for_filtering = 1
minimum_deaths_for_graphing = 5
af = addfips.AddFIPS()
#New York City is not a county- it is same a Bronx county
nyc_fips = af.get_county_fips('bronx', 'New York')
#there is no FIPS for NYC- brox fips is the place holder
data1.fips.fillna(nyc_fips,inplace=True)


df1 = data1[data1["deaths"]>=minimum_deaths_for_filtering]
fips = set(df1["fips"])

data = data1[data1["fips"].isin(fips)]


#put your census API key here
apiKey = "b4f192c09891cbcd149d89bde758036549d5a30f"
#example   https://api.census.gov/data/2019/pep/population?get=POP&for=county:*&in=state:*&key=YOUR_KEY_GOES_HERE
baseurl = 'https://api.census.gov/data/2019/pep/population?get=POP&'
print(baseurl)
population = {}
fips_l = []
pop_l = []
county_l=[]
state_l=[]

for i in fips:
    state_fips = str(int(int(i)/1000)).zfill(2)    
    county_fips = str(int(i)).zfill(5)[2:]
    geography = 'for=county:'+ county_fips + '&in=state:' + state_fips + '&key=' 
    urlapi = baseurl+geography+apiKey
    response = requests.get(urlapi)
    if(response.status_code == 200):
        formattedResponse = json.loads(response.text)[1:]
        population[i]=formattedResponse[0][0]
        row = data[data['fips'] == i].iloc[1]
        print('fips ',str(int(i)).zfill(6), ' st ',state_fips,' ct ',\
              county_fips,' pop ',population[i],' ',\
              row.county,' ',\
              row.state)
        fips_l.append( str(int(i)).zfill(5))
        pop_l.append(population[i])
        county_l.append(row.county)
        state_l.append(row.state)
       
file='../data/fips_pop.csv'
df2 = pd.DataFrame(np.column_stack([fips_l,pop_l,county_l,state_l]),\
                       columns=['fips','pop','county','state'])
df2.to_csv(file,index=False)  
print('Done..............')