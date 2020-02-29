#%%[markdown]
# # Week 12: Exercise 12.2
# File: DSC540_Paulovici_Exercise_12_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 2/26/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 12.2

#%%[markdown]
# Going back to Chapter 12, let’s practice creating a Spider with Scrapy. Follow along with your book, Data Wrangling with Python, starting on page 336-345. Make sure to submit any errors you had, your code and your .csv/.json/.xml file with the data generated.

#%%[markdown]
# ### Create scrapyspider project

# scrapyspider/scrapyspider/items.py, modified for EmojiSpiderItem class <br>
# scrapyspider/scrapyspider/spiders/emo_spider.py, created for EmoSpider class

#%%[markdown]
# ### Test spider

# From scrapyspider run: scrapy crawl emo

#%%[markdown]
# ### Scrapy Shell

# Run the scrapy shell command to test fetch
# fetch('http://www.emoji-cheat-sheet.com')
# test response methods
# update emo_spider.py

#%%[markdown]
# ### Call spider again

# From scrapyspider run: scrapy crawl emo -o items.csv (items.json)