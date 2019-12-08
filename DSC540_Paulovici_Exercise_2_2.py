#%% [markdown]
# # Week 2: Exercise 2.2
# File: DSC540_Paulovici_Exercise_2_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 12/7/2019<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Python Basics

#%% [markdown]
# ## What tools will you be using for the class and which version of Python? Jupyter Notebook, PyCharm, Anaconda, etc.?
# Python version (Anaconda): 3.6.5 <br> <br>
# Editor/IDE: Visual Studio Code <br> <br>
# I will be submitting a Jupyter Notebook, but both a .py and .ipynb file will be available via github. If you prefer just a github link to the assignment please let know.

#%% [markdown]
# ## Complete the following using Python – make sure to show your work and show the values returned. You can submit via your notebook or code editor, no need to export your work.

#%% [markdown]
# ### Change case in a string

#%%
str1 = "hello"

print(str1.capitalize())
print(str1.upper())

#%% [markdown]
# ### Strip space off the end of a string

#%%
str2 = "hello         "
print("{} has {} characters before stripping.".format(str2, len(str2)))

str2 = str2.rstrip()
print("{} now has {} characters.".format(str2, len(str2)))

#%% [markdown]
# ### Split a string

#%%
str3 = "spam sausage spam spam bacon spam tomato and spam"

str3_split = str3.split()

print("Spliting {} results in a {}".format(str3, type(str3_split)))
print(str3_split)

#%% [markdown]
# ### Add and Subtract integers and decimals
num1 = 2
num2 = 1
num3 = 1.1
num4 = 2.5

print("Adding {} + {} = {}".format(num1, num2, num1+num2))
print("Subtracting {} - {} = {}".format(num1, num2, num1-num2))

print("Adding {} + {} = {}".format(num3, num4, num3+num4))
print("Subtracting {} - {} = {}".format(num3, num4, num3-num4))

#%% [markdown]
# ### Create a list

#%%
list1 = ["spam", "spam", "spam", "eggs"]

print(list1)
type(list1)

#%% [markdown]
# ### Add to the list

#%%
print(list1, "before adding bacon")
list1.append("bacon")
print(list1, "after adding bacon")

#%% [markdown]
# ### Subtract from the list

#%%
print(list1, "before removing eggs")
list1.remove("eggs")
print(list1, "after removing eggs")

#%% [markdown]
# ### Remove the last item from the list

#%%
print(list1, "before removing last item")
list1.pop()
print(list1, "after removing last item")

#%% [markdown]
# ### Re-order the list

#%%
# I need a new list for this...
list2 = [2.3, 5, 10, 7, 2, 4]

print(list2, "before re-ordering")
list2.reverse()
print(list2, "after re-ordering")

#%% [markdown]
# ### Sort the list

#%%
print(list2, "before sorting")
print(sorted(list2), "after sorting")

#%% [markdown]
# ### Create a dictionary

#%%
dict1 = {"num1": 1, "num2": 2}

print(dict1)
type(dict1)

#%% [markdown]
# ### Add a key-value to the dictionary

#%%
dict1["num3"] = 3

print(dict1)

#%% [markdown]
# ### Set a new value to corresponding key in dictionary

#%%
dict1["num3"] = "three"

print(dict1)

#%% [markdown]
# ### Look up the new value by the key in dictionary

#%%
print("The value of num3 is: {}.".format(dict1["num3"]))
