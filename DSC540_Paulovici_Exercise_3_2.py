#%% [markdown]
# # Week 3: Exercise 3.2
# File: DSC540_Paulovici_Exercise_3_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 12/15/2019<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 3.2, csv, json, xml, excel 

#%% [markdown]
# ## Data Files
# Data files used for this exercise can be found here: https://github.com/jackiekazil/data-wrangling 

#%%
import csv
import json
from xml.etree import ElementTree as ET 
import xlrd
import pprint

#%% [markdown]
# ## CSV 

#%% [markdown]
# Using Python, import the CSV file provided under Chapter 3 in the GitHub repository using the csv library. Put the data in lists and print each record on its own dictionary row (Hint: Page 51-52 of Data Wrangling with Python).

#%%
# open the csv file
with open("data-text.csv", "r", newline='') as file_in:
    # read the csv file as a dict
    csv_in = csv.DictReader(file_in)

    # print each row of the csv file 
    for row in csv_in:
        pprint.pprint(row)

#%% [markdown]
# ## JSON

#%% [markdown]
# Using Python, import the JSON file provided in the GitHub repository under Chapter 3. Print each record on its own dictionary row (Hint: page 53-54 of Data Wrangling with Python).

#%%
# open the json file
with open("data-text.json", "r") as file_in:
    # read/load the json file
    json_in = json.load(file_in)

    # print each dict
    for d in json_in:
        pprint.pprint(d)

#%% [markdown]
# ## XML

#%% [markdown]
# Using Python, import the XML file provided in the GitHub repository under Chapter 3. Print each record in its own dictionary row (Hint: page 64 of Data Wrangling with Python).

#%%
# read the xml data
tree = ET.parse("data-text.xml")
root = tree.getroot()
data = root.find("Data")

# create list to hold the xml structure
all_data = []

for observation in data:
    record = {}

    for item in observation:
        lookup_key = list(item.attrib)[0]
        
        # Numeric is unique compared to other Categories so it needs special consideration
        if lookup_key == "Numeric":
            rec_key = "NUMERIC"
            rec_value = item.attrib["Numeric"]
        else:
            rec_key = item.attrib[lookup_key]
            rec_value = item.attrib["Code"]

        # add records to the dict
        record[rec_key] = rec_value
    
    # add dict to list
    all_data.append(record)

# print list
pprint.pprint(all_data)

#%% [markdown]
# ## Excel

#%% [markdown]
# Using Python, import the Excel file provided in the GitHub repository under Chapter 4. Print each record in its own dictionary row. (Hint: page 85-88 of Data Wrangling with Python).

#%%
# open the excel file 
excel_file = xlrd.open_workbook("SOWC 2014 Stat Tables_Table 9.xlsx")

# define the sheet to read
table_9 = excel_file.sheet_by_name("Table 9 ") 

# define dict for rows
table_9_data = {}

# loop through the rows, starting with row 14 (data starts)
for i in range(14, table_9.nrows):
    row = table_9.row_values(i)
    country = row[1] # column B

    table_9_data[country] = {
        'child_labor': {
            'total': [row[4], row[5]],
            'male': [row[6], row[7]],
            'female': [row[8], row[9]]
        },
        'child_marriage': {
            'married_by_15': [row[10], row[11]],
            'married_by_18': [row[12], row[13]],
        }
    }

    # Zimbabwe is the last country so break out of loop
    if country == 'Zimbabwe':
        break

pprint.pprint(table_9_data)
