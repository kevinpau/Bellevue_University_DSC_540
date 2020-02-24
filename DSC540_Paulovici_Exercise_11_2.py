#%%[markdown]
# # Week 11: Exercise 11.2
# File: DSC540_Paulovici_Exercise_11_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 2/23/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 11.2

#%% [markdown]
# Going back to Chapter 9 (Data Wrangling with Python), let’s practice joining numerous datasets – an activity you will likely run into frequently. Following the example in your text that starts on page 229 – 233 of Data Wrangling with Python, work through the example to bring two datasets together. Submit your code and output to the assignment link.

#%%
import xlrd
from xlrd.sheet import ctype_text
import agate

# import the UNICEF child labor data
cpi_workbook = xlrd.open_workbook('corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

for r in range(cpi_sheet.nrows):
    print(r, cpi_sheet.row_values(r))

# %%
# get titles
cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]

# get rows
cpi_rows = [cpi_sheet.row_values(r) for r in range (3, cpi_sheet.nrows)]

# data types
text_type = agate.Text()
number_type = agate.Number()
bool_type = agate.Boolean()
date_type = agate.Date()

# get types
def get_types(example_row):
    """ function determines the type of data"""
    types = []

    for v in example_row:
        value_type = ctype_text[v.ctype]
        if value_type == 'text':
            types.append(text_type)
        elif value_type == 'number':
            types.append(number_type)
        elif value_type == 'xldate':
            types.append(date_type)
        else:
            types.append(text_type)

    return types

cpi_types = get_types(cpi_sheet.row(3))

# %%
def get_table(new_arr, types, titles):
    """ function handles errors """
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print(e)

# %%
# create a table of our data
cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

# %%
# to reduce repetetive code, we can import the 'ranked' table from week 7
# This would be a modified version to remove prints and output
from DSC540_Paulovici_Exercise_7_2 import ranked

print(type(ranked))

#%%
# join our child labor data and our cpi_table
cpi_and_cl = cpi_table.join(ranked, 'Country / Territory', 'Countries and areas', inner=True)

cpi_and_cl.column_names
# %%
# print out the first few rows of data
for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print('{}: {} - {}%'.format(r['Country / Territory'], r['CPI 2013 Score'],
    r['Total (%)']))

# %%
