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
from plotnine import *
from plotnine.data import *
    
#getting the initial data
file = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
data1 = pandas.read_csv(file)
del data1["fips"]


#filtering out the counties I don't want to look at
minimum_deaths_for_filtering = 30
minimum_deaths_for_graphing = 5
counties = list(set(data1[data1["deaths"]>minimum_deaths_for_filtering]["county"]))
county = counties
data = data1[data1["county"].isin(county)]
del data["state"]

#separating the data by county into a dictionary, then combining back together
#into a dataframe
data_by_county = {}
for i in county:
    county_data = data[data["county"]==i][data[data["county"]==i]["deaths"]>minimum_deaths_for_graphing]
    county_data.insert(0, "Day", list(range(1, len(county_data)+1)))
    data_by_county[i] = county_data
graphable_data = pandas.DataFrame(columns = data_by_county[county[0]].columns)
for i in data_by_county:
    graphable_data = graphable_data.append(data_by_county[i], ignore_index = True)

#transforming all the integer datatypes into numpy integers
deaths = numpy.asarray(list(graphable_data["deaths"]), dtype=numpy.float64)
days = numpy.asarray(list(graphable_data["Day"]), dtype=numpy.float64)
counties = numpy.asarray(list(graphable_data["county"]))
cases = numpy.asarray(list(graphable_data["cases"]), dtype=numpy.float64)
graphable_data["deaths"] = deaths
graphable_data["Day"] = days
graphable_data["county"] = counties
graphable_data["cases"] = cases

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
os.remove(file1+'.png')
os.remove(file2+'.png')