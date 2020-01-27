#%% [markdown]
# # Week 7: Exercise 7.2
# File: DSC540_Paulovici_Exercise_7_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 1/26/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 7.2

#%%
# import needed libraries
import xlrd
import agate
from xlrd.sheet import ctype_text
import pprint
import matplotlib.pyplot as plt

#%%[markdown]
# ## Load Excel spreasheet data for assignments

#%%
# open spreadsheet and sheet of interest
wb = xlrd.open_workbook("unicef_oct_2014.xls")
wb.nsheets
sheet = wb.sheets()[0]

# get title rows
title_rows = zip(sheet.row_values(4), sheet.row_values(5))

# get title columns
titles = [t[0] + '' + t[1] for t in title_rows]
titles = [t.strip() for t in titles]

# get country rows
country_rows = [sheet.row_values(r) for r in range(6, 114)]

# print titles for reference
pprint.pprint(titles)

#%%[markdown]
# ## Importing Data – (Data Wrangling with Python, Page 219-224)
# Create a function to take an empty list, iterate over the columns and create a full list of all the column types for the dataset. Then load into agate table – make sure to clean the data if you get an error. Follow along with the example in the book on the pages listed.

#%%
# data types
text_type = agate.Text()
number_type = agate.Number()
bool_type = agate.Boolean()
date_type = agate.Date()
example_row = sheet.row(6)

# set data types based on example row
types = []
for v in example_row:
    val_type = ctype_text[v.ctype]

    if val_type == 'text':
        types.append(text_type)
    elif val_type == 'number':
        types.append(number_type)
    elif val_type == 'xldate':
        types.append(date_type)
    else:
        types.append(text_type)

# ERROR
#table = agate.Table(country_rows, titles, types)
# results in CastError - need to clean the data

"""
function to remove bad characters

@param: val (str) - character to be cleaned

return: val (str) - cleaned character  
"""
def remove_bad_chars(val):
    if val == '-':
        return None
    return val

"""
function to generate new array of cleaned data

@param: old_array (list) - rows of data (dirty)
@param: fun_to_clean (function) - function to clean data

return: new_array (list) - clean data
"""
def get_new_array(old_array, fun_to_clean):
    new_array = []
    for row in old_array:
        cleaned_row = [fun_to_clean(rv) for rv in row]
        new_array.append(cleaned_row)
    return new_array

# create new array of cleaned data
cleaned_rows = get_new_array(country_rows, remove_bad_chars)

# load data into agate table & print
table = agate.Table(cleaned_rows, titles, types)
table.print_table(max_columns=7)


#%%[markdown]
# ## Exploring Table Functions – (Data Wrangling with Python, Page 225-228)

#%% [markdown]
# ### 1) Which countries have the highest rates of child labor?

#%%
high_rates = table.order_by('Total (%)', reverse=True).limit(5)

for r in high_rates.rows:
    print(r['Countries and areas'], r['Total (%)'])

#%%[markdown]
# ### 2) Which countries have the most girls working?

#%%
female_data = table.where(lambda r: r['Female'] is not None)
most_females = female_data.order_by('Female', reverse=True).limit(5)

for r in most_females.rows:
    print('{}: {}%'.format(r['Countries and areas'], r['Female']))

#%%[markdown]
# ### 3) What is the average percentage of child labor in cities?
#%%
has_poor = table.where(lambda r: r['Place of residence (%)Urban'] is not None)
avg_percent = has_poor.aggregate(agate.Mean('Place of residence (%)Urban'))

print('Average percentage of child labor in cities: {}%'.format(round(avg_percent, 2)))


#%%[markdown]
# ### 4) Find a row with more than 50% of rural child labor.
#%%
has_poor = table.where(lambda r: r['Rural'] is not None)
first_match = has_poor.find(lambda x: x['Rural'] > 50)

print('The first row with > 50% rural child labor is', first_match['Countries and areas'])

#%%[markdown]
# ### 5) Rank the worst offenders in terms of child labor percentages by country.

#%%
ranked = table.compute([('Total Child Labor Rank', agate.Rank('Total (%)', reverse=True)), ])

for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Total Child Labor Rank'], '\t', row['Countries and areas'], row['Total (%)'])

#%%[markdown]
# ### 6) Calculate the percentage of children not involved in child labor.

#%%
def reverse_percent(row):
    return 100 - row['Total (%)']

ranked = table.compute([('Children not working (%)', agate.Formula(number_type, reverse_percent)),])
ranked = ranked.compute([('Total Child Labor Rank', agate.Rank('Children not working (%)')),])

percent_not_working = ranked.aggregate(agate.Mean('Children not working (%)'))
print('The total % of children not working is {}%'.format(round(percent_not_working, 2)), '\n')

print('The best countries for children not working are:')

for row in ranked.order_by('Total (%)', reverse=False).limit(20).rows:
    print(row['Countries and areas'], row['Total (%)'], row['Children not working (%)'])


#%%[markdown]
# ## Charting with matplotlib – (Data Wrangling with Python, Page 255-258)

#%%[markdown]
# ### Initial setup of data for corruption_perception_index.xls

#%%
# keep float data types as strings
def float_to_str(float):
    return str(float)

def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print(e)

# set up the data types for columns
def get_types(row):
    types = []
    for v in row:
        value_type = ctype_text[v.ctype]
        if value_type == 'text':
            types.append(text_type)
        elif value_type == 'number':
            types.append(number_type)
        elif value_type == 'xldate':
            types.append(date_type)
        else:
            types.append( text_type)
    return types

# open the spreadsheet and sheet of interest
cpi_workbook = xlrd.open_workbook('corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

for r in range(cpi_sheet.nrows):
    #print(r, cpi_sheet.row_values(r))
    cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
    cpi_titles = [t[0] + '' + t[1] for t in cpi_title_rows]
    cpi_titles = [t.strip() for t in cpi_titles]
    cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]
    cpi_types = get_types(cpi_sheet.row(3))

cpi_titles[0] = cpi_titles[0] + ' Duplicate'

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)
cpi_rows = get_new_array(cpi_rows, float_to_str)
cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory', 'Countries and areas', inner=True)

#%%[markdown]
# ### 1) Chart the perceived corruption scores compared to the child labor percentages.

#%%
plt.plot(cpi_and_cl.columns['CPI 2013 Score'], cpi_and_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')
plt.show()

#%%[markdown]
# ### 2) Chart the perceived corruption scores compared to the child labor percentages using only the worst offenders.

#%%
# initial set-up for plotting
cl_mean = cpi_and_cl.aggregate(agate.Mean('Total (%)'))
cpi_mean = cpi_and_cl.aggregate(agate.Mean('CPI 2013 Score'))

def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False

highest_cpi_cl = cpi_and_cl.where(lambda x: highest_rates(x))

#%%
plt.plot(highest_cpi_cl.columns['CPI 2013 Score'], highest_cpi_cl.columns['Total (%)'])
plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')
plt.show()
