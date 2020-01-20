#%% [markdown]
# # Week 6: Midterm Project
# File: DSC540_Paulovici_Midterm.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 1/19/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Midterm Project

#%%[markdown]
# # Tasks
# 1) Replace headers (Data Wrangling with Python pg. 154 – 163) <br>
# 2) Format Data to a Readable Format (Data Wrangling with Python pg. 164 – 168) <br>
# 3) Identify outliers and bad data (Data Wrangling with Python pg. 169 – 174) <br>
# 4) Find Duplicates (Data Wrangling with Python pg. 175 – 178) <br>
# 5) Conduct Fuzzy Matching (if you don’t have an obvious example to do this with in your data, create categories and use Fuzzy Matching to lump data together) (Data Wrangling with Python pg. 179 – 188) <br>
# Summary - A 250-word paper summarizing your steps and any challenges you ran into during the project. You should also outline any decisions you had to make while transforming the data (for example, if you decided to remove duplicates, how did you arrive at that decision?).

#%%[markdown]
# ## Database Info
# Dataset: pokemon.csv retrieved from https://www.kaggle.com/rounakbanik/pokemon <br>
# Note: The dataset contains 802 rows, this was extended to more than the required 1000. This was also done for #4 of the assignment.

#%%
from csv import DictReader
import pprint

#%%[markdown]
# ## Part 1 - Replace headers

#%% 
# open the dataset wiith DictReader
poke_data = DictReader(open('pokemon_data.csv', encoding='ISO-8859-1'))

# create list of all rows
poke_rows = [d for d in poke_data]

pprint.pprint(poke_rows[0])

#%%
""" After looking at the headers, we can replace the "against_" col names with something
else, say "facing_". 
So, we need to make a dict of headers to replace. 
1) Find the the write headers
2) Add as a key to dict, replacement in value 
"""
new_headers = {} 

for data_dict in poke_rows:
    for dkey, dval in data_dict.items():
        # determine if it is a header we want to replace
        if "against_" in dkey:
            new_headers[dkey] = dkey.replace("against_", "facing_")

#%%
""" Search through the dicition, when headers are found that need to be replace. 
Otherwise, leave data as is
"""
new_poke_rows = []

for data_dict in poke_rows:
    new_row = {}
    for dkey, dval in data_dict.items():
        if dkey in new_headers.keys():
            new_row[new_headers[dkey]] = dval
        else:
            new_row[dkey] = dval
    new_poke_rows.append(new_row)

pprint.pprint(new_poke_rows[0])

#%%[markdown]
# ## Part 2 - Format Data to a Readable Format

#%%
""" pprint does provide a fairly clean format as is, however, there is too much data
for general viewing. Let's pick out a select few by searching for them in the newly created data set.
Note - As an example, we don't need to print out all data rows, we'll show a few.
"""
# create list of data to show
select_data = "name type1 type2 hp speed attack defense".split()
count = 0

for data_dict in new_poke_rows:
    if count == 0 or count == 254 or count == 758:
        print("********* New Pokemon *********")

    for dkey, dval in data_dict.items():
        for s in select_data:
            if s == dkey:
                if count == 0 or count == 254 or count == 758:
                    print("{}: {}".format(dkey, dval))
    
    count += 1

#%%[markdown]
# ## Part 3 - Identify outliers and bad data

#%%
""" Given the data, there is expected to be a large variety of ranges in the stats of each
pokemone (e.g., hp can vary from low to high values). However, we identify outliers that 
we may or may not want to keep. is_legendary is column to check if a pokemon is legendary. 
You can argue either way to keep or discard it. For now, I'll just be finding which are legendary.
"""
legendary = 0
non_legendary = 0
# is_legendary = 1, yes
# is_legendary = 0, no
for data_dict in new_poke_rows:
    for dkey, dval in data_dict.items():
        if dkey == "is_legendary":
            if dval == "1":
                legendary += 1
            else:
                non_legendary += 1

print("There are {} legendary Pokemon".format(legendary))
print("There are {} non-legendary Pokemon".format(non_legendary))

# We can see ~10% of the Pokemon can be considered outliers.

#%%[markdown]
# ## Part 4 - Find Duplicates

#%%
""" First we'll check to see if there are any duplicates based on the name col. Other cols will have duplicates and that is expected (e.g., type1 - there is a limited number of options).
"""
# 
unique = [] 
duplicate = 0

for data_dict in new_poke_rows:
    if data_dict["name"] in unique:
        duplicate += 1
    else:
        unique.append(data_dict["name"])

print("There are {} duplicates".format(duplicate))

#%% 
# One way to handle this is to not include them in the new_poke_rows data, so lets 
# adjust the creation of these to exclude them from the beginning

new_poke_rows = []
unique = [] 

for data_dict in poke_rows:
    if data_dict["name"] in unique:
        pass

    else:
        new_row = {}
        for dkey, dval in data_dict.items():
            if dkey in new_headers.keys():
                new_row[new_headers[dkey]] = dval
            else:
                new_row[dkey] = dval
        new_poke_rows.append(new_row)

        unique.append(data_dict["name"])

# now we can re-run the previous loop to check
duplicate = 0
unique = []

for data_dict in new_poke_rows:
    if data_dict["name"] in unique:
        duplicate += 1
    else:
        unique.append(data_dict["name"])

print("There are {} duplicates".format(duplicate))

#%%[markdown]
# ## Part 5 - Conduct Fuzzy Matching

#%%
from fuzzywuzzy import fuzz
import random

#%%
""" To mimic fuzzy matching, I'm going to use a subset of my data, specifically Type2 == "".
Then I'm going to fill the missing spots with variations of "fire" and test how they compare to "fire". I'm also going to exlcude duplicates.
"""
variations = ["FIRE", "fire type", "Fire"]

sub_poke_rows = []
unique = [] 

for data_dict in poke_rows:
    if data_dict["name"] in unique:
        pass
    elif data_dict["type2"] != "":
        pass 
    else:
        type2 = random.choice(variations)
        new_row = {}
        for dkey, dval in data_dict.items():
            if dkey in new_headers.keys():
                new_row[new_headers[dkey]] = dval
            elif dkey == "type2":
                new_row[dkey] = type2
            else:
                new_row[dkey] = dval
        sub_poke_rows.append(new_row)

pprint.pprint(sub_poke_rows[0])

# %%
# TODO - The above code sets up the fuzzy matching, additional code should be added to seach through the sub_poke_rows for all variations. I'm assuming I found them and continuing on the fuzzy matching

#%%
# Fuzzy matching
# TODO - A more detailed loop should be implemented to check more variations then the subset I'm looking at.

compare = "fire"

# ratio
for v in variations:
    ratio = fuzz.ratio(v, compare)
    print("The ratio for {} and {} is: {}".format(v, compare, ratio))

# %%
# partial ratio
for v in variations:
    ratio = fuzz.partial_ratio(v, compare)
    print("The partial ratio for {} and {} is: {}".format(v, compare, ratio))

# %%
# token sort ratio
for v in variations:
    ratio = fuzz.token_sort_ratio(v, compare)
    print("The token sort ratio for {} and {} is: {}".format(v, compare, ratio))

# %%
# token set ratio
for v in variations:
    ratio = fuzz.token_set_ratio(v, compare)
    print("The token set ratio for {} and {} is: {}".format(v, compare, ratio))

# %%[markdown]
# ## Summary

#%%[markdown]
# See DSC540_Paulovici_Midterm_summary.docx