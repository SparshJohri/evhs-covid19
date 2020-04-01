# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 12:45:54 2020

@author: bhata
"""
import pandas
import numpy
import matplotlib.pyplot as plt
import scipy
from plotnine import *
from plotnine.data import *


def rounder(number, place):
    number = int(number * (10**place))
    number = number/(10**place)
    return number
    
#getting the initial data
file = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
data = pandas.read_csv(file)
del data["fips"]


#filtering out the counties I don't want to look at
counties = list(set(data["county"]))
county = ["Bergen", "Broward", "Cook", "Dougherty", "Los Angeles",\
          "Macomb", "Nassau", "New York City", "Oakland", "Orleans", \
          "Santa Clara", "Snohomish","King"]
data = data[data["county"].isin(county)]
del data["state"]
data = data.set_index("date")


#filtering out the counties I don't want to look at

minimum_deaths = 0

data_by_county = {}
for i in county:
    data_by_county[i] = data[data["county"]==i]
    sub = data_by_county[i]
    data_by_county[i] = sub[sub["deaths"]>minimum_deaths]

formatted_list_of_data_by_county = []
for i in county:
    counter = 0
    for j in data_by_county[i].index:
        datapoint = [i, counter, data_by_county[i].loc[j]["deaths"], ]
        counter += 1
        formatted_list_of_data_by_county.append(datapoint)

graphable_data = pandas.DataFrame(formatted_list_of_data_by_county, \
                                  columns = ["County", "Days", "Deaths"])


myPlot = ggplot(graphable_data, aes('Days', 'Deaths', color='factor(County)'))\
 + geom_line(size = 2)\
 + theme(text=element_text(size = 25))
ggsave(myPlot, width = 15, height = 15)
myPlot.draw()