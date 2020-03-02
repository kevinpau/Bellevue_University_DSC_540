#%%[markdown]
# # Week 12: Final Project
# File: DSC540_Paulovici_Final_Porject.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 2/29/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Final Project

#%%[markdown]
# ## Project Outline
# During the course, you will be working on a term project to either pull data from an API or scrape a webpage. You will need to select either an API (different than Twitter) or a Webpage and create a process in Python that will extract data into a formatted dataset. <br><br>
# Part 1: Your formatted dataset with at least 15-20 variables (if the API or Webpage you selected doesn’t have that many fields available on it, you will want to search again, or do multiple!) <br> <br>
# Part 2: Your code or screenshots of your code outlining the steps and process you had to take to pull data from the API or web page and the steps you took to format the data.<br><br>
# Part 3: 2 Data Transformation/Clean-up Steps (can be any that we learned in class)<br><br>
# Part 4: A 250-word paper summarizing your steps and any challenges you ran into during the project. Discuss the importance and relevance of this type of process if you were a data scientist. How often do you think you would have to do this to get the data you need?

#%%[markdown]
# ### Overview
# I'll be working with the https://openweathermap.org/api for this project. <br><br>
# I'll make the assumption that the user will use a zip code from the US to request weather data. Some checks will ensure a valid zip code is provided. <br><br>
# Select variables will be collected from the api, data will be cleaned and transformed into a more usable format (e.g., csv/json/excel)

# %% [markdown]
# ### Part 1 
#%%
# a) Start by requesting a zip code from the user.
user_val = ""
while isinstance(user_val, str): 
    if isinstance(user_val, int):
        break
    else:
        user_val = input("Welcome to the Weather App\nEnter a zip code to get started:")
    
    if len(str(user_val)) == 5:
        try:
            user_val = int(user_val)

        except:
            print("Value entered is not a valid zip code")
            pass
    else:
        print("Value entered is not a valid zip code")

print("The zip code to be used is: {}".format(user_val))

#%%
# b) Before we request data from the API, we'll import our key and set some parameters for the data 
# we'll use some data from our assumption to help create the url.
unit = 'imperial' # units for data
country = 'US' # country
zipFormat = 'http://api.openweathermap.org/data/2.5/weather?zip='

# to protect the API key we'll pull it from another file
from key import getKey
APIKEY = getKey()

print(len(APIKEY))

# %%
# c) Use the zip code to request data from the API

import requests
from pprint import pprint

# build the url 
# api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={your api key}
url = '{}{},{}{}&units={}'.format(zipFormat, user_val, country, APIKEY, unit)

try:
    data = requests.get(url).json()
    pprint(data)
except:
    print("Failed to retrieve weather data")

#%%
# d) Next we'll need to parse the data into a format that is useable. Additionally, we don't need all the values returned. As we go, we can clean and transform the data (e.g., cleaner numbers and correct the date/time associated with sunset/sunrise).

from datetime import datetime

# These list hold the dict key for data we retrieved from the API
coord = ["lat", "lon"]
main = ["feels_like", "humidity", "pressure", "temp", "temp_max", "temp_min"]
name = ["name"]
sys = ["country", "id", "sunrise", "sunset"]
weather = ["description"]
wind = ["speed"]
data_dicts = {"coord":coord, "main":main, "name":name, "sys":sys, "weather":weather, "wind":wind}

# We'll collect all data and set it to a dictionary, first with the API names
select_data = {} 

for d in data_dicts.keys():
    for item in data_dicts[d]:
        if d == "coord":
            val = float(data[d][item])
            select_data[item] = val
        elif d == "main":
            val = float(data[d][item])
            select_data[item] = val
        elif d == "name":
            val = data[d]
            select_data[item] = val
        elif d == "sys":
            val = data[d][item]

            # fix the time stamp
            if item == "sunrise" or item == "sunset":
                date_time = datetime.utcfromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S').split()
                select_data["Date"] = date_time[0]
                val = date_time[1]

            select_data[item] = val
        elif d == "weather":
            val = data[d][0][item]
            select_data[item] = val
        elif d == "wind":
            val = data[d][item]
            select_data[item] = val
        
        else:
            pass
            
pprint(select_data)

#%%
# e) Lastly, we'll want to create better headers and save the data. 

# These are the headers we'll want at the end
cols = ["City", "Country", "Country_id", "Sunrise", "Sunset", 
        "Pressure_(hPa)", "Temperature_Feels_like_(F)", "Temperature_(F)", 
        "Min_Temperature_(F)", "Max_Temperature_(F)", "Humidity_(%)", "Weather_Description", "Wind_Speed_(miles/hr)", "Latitude", "Longitude"]

# mapping of headers
col_dict = {"City":"name", 
"Country":"country", 
"Country_id":"id",  
"Sunrise":"sunrise", 
"Sunset":"sunset", 
"Pressure_(hPa)":"pressure",  
"Temperature_Feels_like_(F)":"feels_like",  
"Temperature_(F)":"temp", 
"Min_Temperature_(F)":"temp_min", 
"Max_Temperature_(F)":"temp_max", 
"Humidity_(%)":"humidity", 
"Weather_Description":"description",
"Wind_Speed_(miles/hr)":"speed", 
"Latitude": "lat",
"Longitude": "lon"}

# new dict with correct headers
clean_data = {}

for k, v in col_dict.items():
    clean_data[k] = select_data[v]

pprint(clean_data)

# save our the clean data.
import csv

with open("weather_data.csv", "w", newline="") as fOut:
    writer =csv.writer(fOut)
    for k, v in clean_data.items():
        writer.writerow([k, v])

# %% [markdown]
# ### Part 2

# Part 1 steps a through e explain step by step the process to retrieve data from the weather API based on a zip code. The data cleaning and transformations are included in this step and will be further explain in Part 3 and 4.


# %% [markdown]
# ### Part 3

# The data transformations were to 1) clean up the dates from Part 1 step d, and 2) transform the headers in Part 1 step e. 

# %% [markdown]
# ### Part 4

# See DSC540_Paulovici_Final_Project.docx for a summary of this project.

#%% [markdown]
# ### Alternative version

# This portion of the code will take the base functionality from above and combine it into a format where the user assumes a set number of zip codes and all values will be added to a since file. <br><br>
# Since this version is an alternative, I will keep comments high level unless it deviates from above version.

#%%
# set the zip codes to check
user_vals = [12302, 10924, 10001,] 

print("Zip codes to check are: {}".format(user_vals))

#%%
# set assumptions for wea ther request 
unit = 'imperial' # units for data
country = 'US' # country
zipFormat = 'http://api.openweathermap.org/data/2.5/weather?zip='

# to protect the API key we'll pull it from another file
from key import getKey
APIKEY = getKey()

#%%
# get requested data and store in a list
req_data = []

import requests
from pprint import pprint

for zip_val in user_vals:
    # build url
    url = '{}{},{}{}&units={}'.format(zipFormat, zip_val, country, APIKEY, unit)

    try:
        data = requests.get(url).json()
        req_data.append(data)
    except:
        print("Failed to retrieve weather data")

#%%
# parse data & collected wanted data

from datetime import datetime

def parse_data(data):
    """ Function takes json data and parses it into a dictionary
    @param data (json) - json format of requested weather data
    return select_data (dict) - dictionary of parsed data 
    """ 
    # These list hold the dict key for data we retrieved from the API
    coord = ["lat", "lon"]
    main = ["feels_like", "humidity", "pressure", "temp", "temp_max", "temp_min"]
    name = ["name"]
    sys = ["country", "id", "sunrise", "sunset"]
    weather = ["description"]
    wind = ["speed"]
    data_dicts = {"coord":coord, "main":main, "name":name, "sys":sys, "weather":weather, "wind":wind}

    # We'll collect all data and set it to a dictionary, first with the API names
    select_data = {} 

    for d in data_dicts.keys():
        for item in data_dicts[d]:
            if d == "coord":
                val = float(data[d][item])
                select_data[item] = val
            elif d == "main":
                val = float(data[d][item])
                select_data[item] = val
            elif d == "name":
                val = data[d]
                select_data[item] = val
            elif d == "sys":
                val = data[d][item]

                # fix the time stamp
                if item == "sunrise" or item == "sunset":
                    date_time = datetime.utcfromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S').split()
                    select_data["Date"] = date_time[0]
                    val = date_time[1]

                select_data[item] = val
            elif d == "weather":
                val = data[d][0][item]
                select_data[item] = val
            elif d == "wind":
                val = data[d][item]
                select_data[item] = val
            
            else:
                pass   
    return select_data

# we'll loop through our data and add the parsed data (dict) to a new list
req_parsed_data = []

for d in req_data:
    req_parsed_data.append(parse_data(d))

#%%
# Next we need to swap our headers

# These are the headers we'll want at the end
cols = ["City", "Country", "Country_id", "Sunrise", "Sunset", 
        "Pressure_(hPa)", "Temperature_Feels_like_(F)", "Temperature_(F)", 
        "Min_Temperature_(F)", "Max_Temperature_(F)", "Humidity_(%)", "Weather_Description", "Wind_Speed_(miles/hr)", "Latitude", "Longitude"]

# mapping of headers
col_dict = {"City":"name", 
"Country":"country", 
"Country_id":"id",  
"Sunrise":"sunrise", 
"Sunset":"sunset", 
"Pressure_(hPa)":"pressure",  
"Temperature_Feels_like_(F)":"feels_like",  
"Temperature_(F)":"temp", 
"Min_Temperature_(F)":"temp_min", 
"Max_Temperature_(F)":"temp_max", 
"Humidity_(%)":"humidity", 
"Weather_Description":"description",
"Wind_Speed_(miles/hr)":"speed", 
"Latitude": "lat",
"Longitude": "lon"}

all_clean_data = {}

for d in req_parsed_data:
    clean_data = {}

    # clean data set
    for k,v in col_dict.items():
        clean_data[k] = d[v]

    # take clean data and add it to all_clean_data
    for k, v in clean_data.items():
        temp = []
        temp.append(v)

        try:
            for items in all_clean_data[k]:
                temp.append(items)
        except:
            pass
        
        all_clean_data[k] = temp

pprint(all_clean_data)

#%%
# Lastly, save out all of our combined clean data
import pandas as pd

df = pd.DataFrame({k: pd.Series(v) for k, v in all_clean_data.items()})
df.to_csv("weather_data2.csv", encoding='utf-8', index=False)
