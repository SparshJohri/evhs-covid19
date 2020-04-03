# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 15:41:27 2020

@author: bhata
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 12:45:54 2020




@author: bhata
"""
import pandas
import numpy
import os
import addfips
import requests
import json
import sys
from time import sleep


from plotnine import *
from plotnine.data import *
    
#getting the initial data
file = "../covid-19-data/us-counties.csv"
data1 = pandas.read_csv(file)


#filtering out the counties I don't want to look at
minimum_deaths_for_filtering = 30
minimum_deaths_for_graphing = 1
af = addfips.AddFIPS()
#New York City is not a county- it is same a Bronx county
nyc_fips = af.get_county_fips('bronx', 'New York')
#there is no FIPS for NYC- brox fips is the place holder
data1.fips.fillna(nyc_fips,inplace=True)

allowed_c=[]
allowed_c =['Los Angeles','Santa Clara', 'San Diego', 'San Francisco', 'King']
print('1')
#allowed_c =['Los Angeles','San Francisco']

df1 = data1[data1["deaths"]>=minimum_deaths_for_filtering]

fips = list(set(df1["fips"]))
if(len(allowed_c)>0):
    data = data1[data1["county"].isin(allowed_c)]
print('2')

df_pop = pandas.read_csv('../data/fips_pop.csv') 


#separating the data by county into a dictionary, then combining back together
#into a dataframe
data_by_fips = {}
last_fips=''
for i in fips:
    fips_data = data[data["fips"]==i][data[data["fips"]==i]["deaths"]>minimum_deaths_for_graphing]
    if len( fips_data) == 0:
        continue
    print('3 ',i)
    fips_data.insert(0, "Day", list(range(1, len(fips_data)+1)))
    df_pop_r = df_pop[df_pop['fips'] == i]
    county_pop=df_pop_r.iloc[0,1]
    print(county_pop, data[data["fips"]==i].iloc[0]["county"])
    c_l=fips_data['cases'].to_list()
    c_l = c_l/county_pop*100 
    fips_data.insert(0, "casepct", c_l)
    data_by_fips[i] = fips_data
    last_fips=i

graphable_data = pandas.DataFrame(columns = data_by_fips[last_fips].columns)
for i in data_by_fips:
    graphable_data = graphable_data.append(data_by_fips[i], ignore_index = True)

#transforming all the integer datatypes into numpy integers
deaths = numpy.asarray(list(graphable_data["deaths"]), dtype=numpy.float64)
days = numpy.asarray(list(graphable_data["Day"]), dtype=numpy.float64)
counties = numpy.asarray(list(graphable_data["county"]))
cases = numpy.asarray(list(graphable_data["cases"]), dtype=numpy.float64)
print('here')
casepct = numpy.asarray(list(graphable_data["casepct"]), dtype=numpy.float64)
print('here.........')
graphable_data["deaths"] = deaths
graphable_data["Day"] = days
graphable_data["county"] = counties
graphable_data["cases"] = cases
graphable_data["casepct"] = casepct



#constants for printing out the graph
text_size = 12
graph_w = 20
graph_h = 8

#Cases per day
file1="temp1"
myPlot = ggplot(graphable_data, aes('Day', 'cases', color="county"))\
 + geom_line(size = 2)\
 + theme(text=element_text(size = text_size))
ggsave(myPlot, filename=file1, width = graph_w, height = graph_h)
myPlot.draw()

#Deaths per day
myPlot = ggplot(graphable_data, aes('Day', 'deaths', color="county"))\
 + geom_line(size = 2)\
 + theme(text=element_text(size = text_size))
file2 = 'temp2'
ggsave( myPlot,filename=file2, width = graph_w, height = graph_h)

myPlot.draw()

#casepct per day
myPlot = ggplot(graphable_data, aes('Day', 'casepct', color="county"))\
 + geom_line(size = 2)\
 + theme(text=element_text(size = text_size))
file3 = 'temp3'
ggsave( myPlot,filename=file2, width = graph_w, height = graph_h)

myPlot.draw()

os.remove(file1+'.png')
os.remove(file2+'.png')
os.remove(file3+'.png')