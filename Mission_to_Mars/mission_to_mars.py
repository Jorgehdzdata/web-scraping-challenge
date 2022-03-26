#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Importing libraries
import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import warnings
warnings.filterwarnings('ignore')
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


#Establsih path to chrome executable file
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News
# 
# [NASA - Mars Exploration Program](https://mars.nasa.gov/news/)
# 
# 
# 

# In[4]:


# Visit the NASA Mars News Page
# Set up url
nasa_url = "https://mars.nasa.gov/news/"
browser.visit(nasa_url)

# Wait for the page/page elements to load.
time.sleep(1)

# Scrape page into soup.
html = browser.html
soup = bs(html, "html.parser")


# In[5]:


# Get latest news title and paragraph text.
news_title = soup.find_all('div', class_='content_title')[1].text
news_p = soup.find_all('div', class_="article_teaser_body")[0].text
print(f"Latest news title: {news_title}.")
print(f"Latest news p text: {news_p}")


# ## JPL Mars Space Images - Featured Image

# In[6]:


# Navigate to the page
img_url = 'https://spaceimages-mars.com/'
browser.visit(img_url)


# Find figure to retrieve section that has image url
jpl_html = browser.html
jpl_soup = bs(jpl_html, "html.parser")
jpl_img_result = jpl_soup.find("a", class_="showimg fancybox-thumbs")
jpl_img_result1 = jpl_img_result["href"]


# In[7]:


# Find the image url to the full size .jpg image
featured_image_url = img_url + jpl_img_result1
featured_image_url


# ## Mars Facts

# In[23]:


# Visit url for mars facts.
url = "https://galaxyfacts-mars.com/"
browser.visit(url)

# Wait for page/page elements to load.
time.sleep(1)


facts_df = pd.read_html(url)[0]
facts_df.columns = ["description","value","earth"]
facts_df = facts_df.drop("earth" , 1)
facts_df = facts_df.set_index("description")
facts_df = facts_df.iloc[1: , :]
facts_df
# Use Pandas to convert the data to a HTML table string.
html_table = facts_df.to_html()

# Strip newlines
html_table.replace("\n","")

# Save html table
facts_df.to_html('mars_facts.html')


# ## Mars Hemispheres

# In[33]:


# Visit url for images of Mar's hemispheres.
base_url = "https://marshemispheres.com/"
h_url_root = base_url.split('/search')[0]
browser.visit(base_url)


# In[34]:


# Wait for the page/page elements to load.
time.sleep(1)

# Scrape page into soup.
html = browser.html
soup = bs(html, "html.parser")


# In[27]:


# Get hemisphere name and image url for the full resolution image.
hemispheres = soup.find_all('div', class_='item')
hemisphere_image_urls = []

for hemisphere in hemispheres:
    link_text = hemisphere.find('h3').text
    splitted = link_text.split('Enhanced')
    title = splitted[0]
    browser.click_link_by_partial_text(link_text)
    hemisphere_page_html = browser.html
    soup = bs(hemisphere_page_html, "html.parser")
    downloads = soup.find('div', class_="downloads")
    img_url = downloads.a["href"]
    hemisphere_dict = { "title": title, "img_url": img_url }
    hemisphere_image_urls.append(hemisphere_dict)
    browser.back()
    
pprint(hemisphere_image_urls)


# In[35]:


# Scrape the site and visit each hemisphere page
title_list = []
url_list = []
    
for result in range(1):
    h_html = browser.html
    h_soup = bs(h_html, "html.parser")
    h_results = h_soup.find_all("div", class_="item")
    
    # Get url for each hemisphere
    for item in h_results:
        item_url = item.a["href"]
        item_full_url = h_url_root + item_url
        url_list.append(item_full_url)
        title = item.find("h3").text
        title_list.append(title)
        
title_list


# In[36]:


# Get image url from each page and create url list
url_dict_list = []

for item_url in url_list:
    browser.visit(item_url)
    html = browser.html
    soup = bs(html, "html.parser")
    img_path = soup.select_one("ul")
    image_url = img_path.a["href"]
    url_dict_list.append(image_url)
    
url_dict_list


# In[38]:


# Combine 2 lists to get one list of dictionaries
hemisphere_image_urls = []

for url,title in zip(url_dict_list,title_list):
    hemisphere_image_dict = {}
    hemisphere_image_dict["title"] = title
    hemisphere_image_dict["img_url"] = url
    hemisphere_image_urls.append(hemisphere_image_dict)
pprint(hemisphere_image_urls)


# !jupyter nbconvert --to script mission_to_mars.ipynb

