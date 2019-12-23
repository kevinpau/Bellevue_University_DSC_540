#%% [markdown]
# # Week 4: Exercise 4.2
# File: DSC540_Paulovici_Exercise_4_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 12/22/2019<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 4.2, PDF and Database

#%% [markdown]
# ## Data Files
# Data files used for this exercise can be found here: https://github.com/jackiekazil/data-wrangling 

#%%
import slate3k as slate
import pdfminer
import pprint
import dataset

#%% [markdown]
# ## PDF Reading

#%% [markdown]
# Follow along with the book and complete the exercise that uses the Slate library starting on page 94 until page 114 (Data Wrangling with Python). At the end of the exercise, the author explains that they’ve run into a roadblock in the code and troubleshooting is the next step. Turn in what you have completed so far with the exercise (make sure to show your work). <br> <br>

# For extra credit, see if you can get better results and a cleaner process working without having data land in the wrong columns. This is the challenge with data like a PDF – there aren’t necessarily the same rules that can be counted on each time and as mentioned above, sometimes manual manipulation ends up being the fastest way to deal with the data.

#%% [markdown]
# ### Opening and Reading Using slate3k

#%%
# open up the pdf file and print out a few pages using slate lib
pdf = 'EN-FINAL Table 9.pdf'

with open (pdf, 'rb') as f:
    doc = slate.PDF(f)
    doc = [w.replace('\n', '') for w in doc] # fix for some the warnings

for page in doc[:2]:
    #print(page)
    print(type(page))

#%% [markdown]
# ### Converting PDF to Text

#%%
# convert pdf file to text
#pdf2txt.py -o en-final-table9.txt EN-FINAL\ Table\ 9.pdf

# text file also available from github link

pdf_text = 'en-final-table9.txt'
openfile = open(pdf_text, 'r')

# adding a count to only print out a few lines
count = 0

for line in openfile:
    if count < 5:
        print(line)
    
    count += 1

#%% [markdown]
# ### Parsing PDFs Using pdfminer

#%%
# code reorganized from book b/c it is run in jupyter not as python script

def turn_on_off(line, status, start, prev_line, end='\n'):
    """
    This function checks to see if a line starts/ends with a certain
    value. If the line starts/ends with that value, the status is
    set to on/off (True/False).
    """
    if line.startswith(start):
        status = True
    elif status:
        if line == end and prev_line != 'and areas':
            status = False
    return status

def clean(line):
    """
    Cleans line breaks, spaces, and special characters from our line.
    """
    line = line.strip('\n').strip()
    line = line.replace('\xe2\x80\x93', '-')
    line = line.replace('\xe2\x80\x99', '\'')
    return line

# start by opening the pdf text file
pdf_txt = 'en-final-table9.txt'
openfile = open(pdf_txt, 'r')

# set values to false to act as flags
country_line = total_line = False

previous_line = ''

# create empty lists to hold values
countries = []
totals = []

# countries that near special consideration
double_lined_countries = [
    'Bolivia (Plurinational \n',
    'Democratic People\xe2\x80\x99s \n',
    'Democratic Republic \n',
    'Lao People\xe2\x80\x99s Democratic \n',
    'Micronesia (Federated \n',
    'Saint Vincent and \n',
    'The former Yugoslav \n',
    'United Republic \n',
    'Venezuela (Bolivarian \n']

# loop through each line to find country and values
for line in openfile:
    if country_line:
        if previous_line in double_lined_countries:
            line = ' '.join([clean(previous_line), clean(line)])
        countries.append(clean(line))

    elif total_line:
        if len(line.replace('\n', '').strip()) > 0:
            totals.append(clean(line))

    country_line = turn_on_off(line, country_line, 'and areas', previous_line)
    total_line = turn_on_off(line, total_line, 'total', previous_line)

    previous_line = line

# print out a dictionary obj of items
data = dict(zip(countries, totals))
pprint.pprint(data)

#%% [markdown]
# ## Database

#%% [markdown]
# Setup a local database with Python and load in a dataset (can be any dataset). You can choose what back-end to use, if you have never done this before, the book recommends SQLite and to follow along with the book, you can find that at: SQLite. <br>
# Create a Python dictionary of the data
# Create a new table.
# Insert the data into that table

#%%
# code based on page 145

# connect to db
db = dataset.connect('sqlite:///data_wrangling1.db')

# dictionary of data
my_data_source = {
    'url': 'http://www.tsmplug.com/football/premier-leaqu-player-salaries-club-by-club/',
    'description': 'Premier League Club Salareies',
    'topic': 'football',
    'verified': False,
    }

# creates a new table called data_sources
table = db['data_sources']

# inserts the dict data into the table 
table.insert(my_data_source)

#%%
# print data from table
for d in db['data_sources']:
    pprint.pprint(d)

#%%
# print columns
print(db['data_sources'].columns)
