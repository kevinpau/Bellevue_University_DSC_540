#%% [markdown]
# # Week 8: Exercise 8.2
# File: DSC540_Paulovici_Exercise_8_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 2/2/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 8.2

#%%[markdown]
# ## Part 1
# Connect to the Internet using Python Library urllib (Data Wrangling with Python? pg 298-300), follow the example in the book to connect to the same website or a different website and submit your code.

#%%
import urllib.parse as urllib
import urllib.request as urllib2
from pprint import pprint

# open and read Google page
google = urllib2.urlopen('http://google.com')
google = google.read()
pprint(google[:200])

# open a web page with query strings
url = 'http://google.com?q='
url_with_query = url + urllib.quote_plus('python web scraping')

web_search = urllib2.urlopen(url_with_query)
web_search = web_search.read()
print('\n')
pprint(web_search[:200])

#%%
# requests tools example
import requests

google = requests.get('http://google.com')
pprint(google.status_code)
pprint(google.content[:200])
pprint(google.headers)
pprint(google.cookies.items())

#%%[markdown]
# ## Part 2
# Reading a Web Page with Beautiful Soup – following the example starting on page 300-304 of Data Wrangling with Python, use the Beautiful Soup Python library to scrap a web page. The result should be data and output in an organized format. Each of the data entries should be in its own dictionary with matching keys.

#%%
# open and read the page with beautiful soup
from bs4 import BeautifulSoup
import requests

page = requests.get('http://www.enoughproject.org/take_action')
bs = BeautifulSoup(page.content)

print(bs.title)
print(bs.findAll('a'))
print(bs.find_all('p'))

#%%
# check relationships on the page
# header_children = [c for c in bs.head.children]
# print(header_children)

# navigation_bar = bs.find(id='globalNavigation')

# for d in navigation_bar.descendants:
#     print(d)

#     for s in d.previous_siblings:
#         print(s)

#%%
# open and read the page with beautiful soup
from bs4 import BeautifulSoup
import requests

page = requests.get('http://www.enoughproject.org/take_action')
bs = BeautifulSoup(page.content, 'html.parser')

ta_divs = bs.find_all('div', class_='wpb_text_column')
print(len(ta_divs))

for ta in ta_divs:
    title = ta.h2
    link = ta.a
    about = ta.find_all('p')   
    print(title, link, about)

#%%
# open and read the page with beautiful soup
from bs4 import BeautifulSoup
import urllib.request

page = urllib.request.urlopen('http://www.enoughproject.org/take_action').read()
bs = BeautifulSoup(page, 'html.parser')

ta_divs = bs.find_all('div', class_='wpb_text_column')
print(len(ta_divs))

for ta in ta_divs:
    print(ta)

# TODO: my get methods are not functional- not sure why 
# use a dictionary for data
# all_data = []

# for ta in ta_divs:
#     data_dict = {}
#     data_dict['title'] = ta.h2.get_text()
#     data_dict['link'] = ta.a.get('href')
#     data_dict['about'] = [p.get_text() for p in ta.find_all('p')]
#     all_data.append(data_dict)

# print(all_data)

#%%[markdown]
# ## Part 3
# Web scraping with Selenium - Follow along with your book starting on page 318-329 of Data Wrangling with Python. At the end of the exercise, you should be able to go to a site, fill out a form, submit the form, and then scroll through the results with the code you wrote. Make sure to submit the code and your output.

#%%
from selenium import webdriver

browser = webdriver.Chrome()

browser.get('http://www.fairphone.com/we-are-fairphone/')
browser.maximize_window()

content = browser.find_element_by_css_selector('li.feed-item') 
print (content.text)
all_bubbles = browser.find_elements_by_css_selector('li.feed-item') 

for bubble in all_bubbles: 
    print (bubble.text)

# %%
from selenium.common.exceptions import NoSuchElementException

all_data = []

for elem in all_bubbles: 
        elem_dict = {}

        elem_dict['text_content'] = \
            elem.find_element_by_css_selector('div.j-message').text
        
        elem_dict['description'] = elem.find_element_by_css_selector('li.feed-item img').get_attribute('alt')
        
        elem_dict['original_link'] = \
            elem.find_element_by_css_selector('li.feed-item a').get_attribute('href') 
        
        try:
            elem_dict['picture'] = elem.find_element_by_css_selector('li.feed-item img').get_attribute('src')
        except NoSuchElementException: 
            elem_dict['picture'] = None
        all_data.append(elem_dict)

#%%
from selenium.common.exceptions import NoSuchElementException

all_data = []
all_bubbles = browser.find_elements_by_css_selector('li.feed-item') 

for elem in all_bubbles:
    elem_dict = {'text_content': None, 'description': None, 'original_link': None, 'picture': None}
    
    content = browser.find_element_by_css_selector('li.feed-item')  
    
    try:
        elem_dict['text_content'] = \
            content.find_element_by_css_selector('div.j-message').text
    except NoSuchElementException: 
        pass
    try:
        elem_dict['description'] = elem.find_element_by_css_selector('li.feed-item img').get_attribute('alt') 
    except NoSuchElementException:
        pass 
    try:
        elem_dict['original_link'] = \
            elem.find_element_by_css_selector('li.feed-item a').get_attribute('href') 
    except NoSuchElementException:
        pass 
    try:
        elem_dict['picture'] = elem.find_element_by_css_selector('li.feed-item img').get_attribute('src')
    except NoSuchElementException: 
        pass
    all_data.append(elem_dict)

#%%
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver

def find_text_element(html_element, element_css): 
    try:
        return html_element.find_element_by_css_selector(element_css).text
    except NoSuchElementException: 
        pass
    return None

def find_attr_element(html_element, element_css, attr): 
    try:
        return html_element.find_element_by_css_selector(element_css).get_attribute(attr)
    except NoSuchElementException: 
        pass
    return None

def get_browser():
    browser = webdriver.Chrome() 
    return browser

def main():
    browser = get_browser() 
    browser.get('http://apps.twinesocial.com/fairphone')
    
    all_data = [] 
    browser.implicitly_wait(10) 
    
    try:
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border') 
    except WebDriverException:
        browser.implicitly_wait(5)
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')  
        
    for elem in all_bubbles:
        elem_dict = {}
        content = elem.find_element_by_css_selector('div.content')
        elem_dict['full_name'] = find_text_element(
            content, 'div.fullname')
        elem_dict['short_name'] = find_attr_element(
            content, 'div.name', 'innerHTML')
        elem_dict['text_content'] = find_text_element(
            content, 'div.twine-description')
        elem_dict['timestamp'] = find_attr_element(
            elem, 'div.when a abbr.timeago', 'title')
        elem_dict['original_link'] = find_attr_element(
            elem, 'div.when a', 'data-href')
        elem_dict['picture'] = find_attr_element(
            content, 'div.picture img', 'src')
        all_data.append(elem_dict)
    browser.quit() 
    return all_data

if __name__ == '__main__': 
    all_data = main() 
    print (all_data)

#%%
from selenium import webdriver 
from time import sleep
    
browser = webdriver.Chrome()
browser.get('http://google.com')
inputs = browser.find_elements_by_css_selector('form input') 

for i in inputs:
    if i.is_displayed(): 
        search_bar = i
        break
        
search_bar.send_keys('web scraping with python')

#search_button = browser.find_element_by_css_selector('.FPdoLc > center:nth-child(1) > input:nth-child(1)')
search_button = browser.find_element_by_css_selector('tsf > div:nth-child(2) > div.A8SBwf.emcav > div.UUbT9 > div.aajZCb > div.tfB0Bf > center > input.gNO89b')
#inspect element > right-click that line > Copy > CSS Selector
search_button.click()

browser.implicitly_wait(10)
results = browser.find_elements_by_css_selector('div.bkWMgd h2')

for r in results:
    browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});",r)
    action = webdriver.ActionChains(browser) 
    action.move_to_element(r) 
    action.perform()
    sleep(2)
    
browser.quit()