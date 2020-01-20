#%% [markdown]
# # Week 6: Exercise 6.2
# File: DSC540_Paulovici_Exercise_6_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 1/19/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 6.2

#%% [markdown]
# ## Data Files
# Data files used for this exercise can be found here: https://github.com/jackiekazil/data-wrangling 

#%% [markdown]
# ## Fixing Labels/Headers (page 155 – 156 Data Wrangling with Python)
# Create a new dictionary for each row to create a new array <br>
# If you don’t want to use the method outlined in the example on page 155-156 Data Wrangling with Python, you could also use Zipping Questions and Answers as a method (page 157-163 Data Wrangling with Python).

#%%
from csv import DictReader
from csv import reader
import pprint

# read in the orig csv data and the headers to be replaced
data_rdr = DictReader(open('mn.csv', encoding='ISO-8859-1'))
header_rdr = DictReader(open('mn_headers.csv', encoding='ISO-8859-1'))

# create list of rows for each data file
data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

# TODO - option print out 
#pprint.pprint(data_rows[:1])
#pprint.pprint(header_rows[:1])

# create a new dictionary for each row to create a new array
new_rows = []

# this portion looks headers to be replace
# additionally, only questions are retained
for data_dict in data_rows:
    new_row = {}
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            if dkey in header_dict.values():
                if header_dict['Question'] != '':
                    new_row[header_dict.get('Label')] = dval
    new_rows.append(new_row)

#%% [markdown]
# ## Data Formats Readable (page 164-165 Data Wrangling with Python)
# Using the same dataset as the above example (mn.csv and mn_headers.csv), use the format method to make output human readable.

#%%
# output of the new_rows array, limited to 1 as an example
for row in new_rows[:1]:
    print("******** ROW (person) ********")

    for dict_item in row.items():
        print("Questions: {0[0]}\n Answer: {0[1]}".format(dict_item))


#%% [markdown]
# ## Data Formatting (page 167-169 Data Wrangling with Python)
# Format the dates to determine when the interview started and ended.

#%%
count = 0

# loop over data_rows to find the times
for data_dict in data_rows:

    # create array for start/end dates
    start_date = []
    end_date = []

    # only use completed interviews
    if data_dict["MWM7"] == "Completed":
        for dkey, dval in data_dict.items():

            # day, month, year format
            if dkey == "MWM6D" or dkey == "MWM6M" or dkey == "MWM6Y":
                start_date.append(dval)
                end_date.append(dval) # interviews completed same day

            # find the time of start / end, hr:min
            if dkey == "MWM10H" or dkey == "MWM10M":
                start_date.append(dval)
            if dkey == "MWM11H" or dkey == "MWM11M":
                end_date.append(dval)

        # build the date string to print
        start = '{0[0]}/{0[1]}/{0[2]} {0[3]}:{0[4]}'.format(start_date)
        end = '{0[0]}/{0[1]}/{0[2]} {0[3]}:{0[4]}'.format(end_date)

        # only print out a few as an example
        if count < 5:
            # print out the dates
            print("****** Interview ******")
            print("Interview start time:", start)
            print("Interview end time:", end)
            print("***********************")

            count += 1

#%% [markdown]
# ## Documentation (page 208-212 Data Wrangling with Python)
# Practice adding documentation to your code following best practices and guidance from your book. You can use previous code from the above examples, or another code example from class

#%%[markdown]
# Documentation of comments and clearly labeled variables is used throughout code. I strive to make simple logical comments without over commentting on trivial code (which I expect a code reviewer to understand). Loops and logic are kept to a minimum without too much complexity to ease the reader on the function.