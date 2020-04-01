import glob
import os
from datetime import datetime
import pandas as pd 

from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap
from plotnine.data import mtcars
from plotnine import *

#data cloned from https://github.com/CSSEGISandData/COVID-19.git
mypath = "..\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports"
os.chdir(mypath)
ext = "*.csv"
#extract all the names of the csv files and extract date from the names
onlyfiles =glob.glob(ext)

#now read each file and put in 3D pandas frame
dict_data_f = {}

for file in onlyfiles:
    data_f = pd.read_csv(file)
    dateobj =  datetime.strptime(file.split('.')[0],'%m-%d-%Y').date()
    dict_data_f[dateobj] = data_f

for key in dict_data_f:
    #header format changed on this date
    format_change_date = '3-22-2020'
    d1 = datetime.strptime(format_change_date,'%m-%d-%Y').date()
    prov = 'Province/State'
    if( key >= d1 ):
        prov = 'Province_State'     
    
    fr = dict_data_f[key]
    province = 'Hubei'
    conf = fr[ fr[prov] == province ]
    conf_val = conf.iloc[0]['Confirmed']
    print(key, '  ',province,'  ',conf_val)

