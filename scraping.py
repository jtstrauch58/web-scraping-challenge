import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from re import search
import time
import pandas as pd

def scrape_info():

# ******************************************************************************
# ******************************************************************************
# Fetch latest articles from NASA site using Beautifulsoup
# ******************************************************************************
# ****************************************************************************** 

    # Set up requests for NASA data 
    url_nasa = 'https://mars.nasa.gov/#news_and_events'
    response_nasa = requests.get(url_nasa)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_nasa = bs(response_nasa.text, 'html.parser')

    # Find top stories using find_all, h3 tag and class - 'title'
    results_nasa = soup_nasa.find_all('h3', class_='title')

    # set up list and dictionary to store the NASA articles
    nasa_news = {}
    
    article_title = []
    article_link = []

    # assign article title and url to lists
    for result in results_nasa:

        try:
            # Identify and return title of listing
            title = result.a.text

            # Identify and return link to listing
            link = result.a['href']
            if search('http', link):
                link = link
            else:
                link = url_nasa + link

            # Append results only if title and link are available
            if (title and link):
                article_title.append(title)
                article_link.append(link)
        except AttributeError as e:
            print(e)

    # import lists into nasa_news dictionary
    nasa_news['nasa'] = {'title': article_title, 'src': article_link}

# ******************************************************************************
# ******************************************************************************
# Fetch latest image url from JPL site using  splinter
# ******************************************************************************
# ******************************************************************************

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Retrieve page with the requests module
    url_jpl = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_jpl)

    # click on "FULL IMAGE" to gain access to the featured picture data
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # assign image url to variable
    mars_img_url = browser.find_by_css('img.headerimage.fade-in')['src']

    browser.quit()

    mars_img = {'title': 'JPL Features Mars Image', 'src': mars_img_url}

    nasa_news['mars'] = {'title': 'JPL Featured Image', 'src': mars_img_url}
    # nasa_news['title_JPL'] = 'JPL Featured Mars Image'
    # nasa_news['src_JPL'] = mars_img_url


# ******************************************************************************
# ******************************************************************************
# Fetch Mars hemisphere image urls from astogeology site using splinter
# and beautifulsoup
# ******************************************************************************
# ******************************************************************************


    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Use splinter to capture hemisphere data
    url_mars_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Setup dictionary and list variables
    img_data = {}
    title = []
    img = []

    # parse url to add to the image cache links
    new = url_mars_hemi.split('/')
    url_recon = new[0] + '//' + new[2]

    # start loop through four hemispheres
    # use splinter to select each image url in order to capture the source url correctly
    # use beautifulsoup to capture data

    hemis = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    for i in range(4):
        
        url_mars_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_mars_hemi)

        time.sleep(5)

        browser.links.find_by_partial_text(hemis[i]).click()
        new_url = browser.url
        response_title = requests.get(new_url)
        # Create BeautifulSoup object; parse with 'html.parser'

        soup_title = bs(response_title.text, 'html.parser')
        # results are returned as an iterable list

        hemi_title = soup_title.find('head')
        title.append(hemi_title.title.text)

        hemi_img = soup_title.find('img', class_='thumb')
        img.append(url_recon + hemi_img['src'])
        
        i += 1

    browser.quit()

    # img_data['title'].append(title)
    # img_data['img'].append(img)

    for index in range(len(title)):
        title[index] = title[index].split(" | ")[0]
        title[index] = title[index].replace(' Enhanced','')

    nasa_news['hemi'] = {'name': title, 'src': img}
    # nasa_news['hemi_title'] = img_data['title']
    # nasa_news['hemi_img'] = img_data['img']

# ********************************************************************************
# ********************************************************************************
# Get data tables about Mars from Space Facts site
# ********************************************************************************
# ********************************************************************************

    # Use pandas to read the tables on the site
    url_mars = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_mars)
    mars_data_tb = tables[0]
    mars_earth_tb = tables[1]

    # Rename columns
    mars_data_tb.rename(columns={0:'Attribute', 1:'Value'}, inplace = True)
    mars_data_tb.set_index('Attribute', inplace = True)

    mars_earth_tb.rename(columns={'Mars - Earth Comparison':'Attribute'}, inplace = True)
    mars_earth_tb.set_index('Attribute', inplace = True)

    # generate HTML code for each table
    mars_earth_html = mars_earth_tb.to_html(header = False, index_names = False, justify = 'left')
    mars_data_html = mars_data_tb.to_html(header = False, index_names = False, justify = 'left')

    nasa_news['mars_facts'] = mars_data_html
    nasa_news['mars_earth_facts'] = mars_earth_html

    return nasa_news
