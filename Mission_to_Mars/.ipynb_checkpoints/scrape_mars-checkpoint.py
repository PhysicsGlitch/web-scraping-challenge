from bs4 import BeautifulSoup as bs
import pymongo
import requests
import pandas as pd
from splinter import Browser
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def soup_scrape(url, db_name):
    response = requests.get(url)
    return(bs(response.text, 'lxml'))

@app.route("/scrape")
def scrape_mars_data():
    
    mars_browser = init_browser()
    
    nasa_url = 'https://mars.nasa.gov/news/8744/nasa-engineers-checking-insights-weather-sensors/'
    mars_facts_url = 'https://space-facts.com/mars/'
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    

    nasa_scrape = soup_scrape(nasa_url, 'nasa_db')
    
    nasa_title = nasa_scrape.title.text

    nasa_paragraphs = nasa_scrape.find_all('p')
    
    executable_path = {"executable_path": 'chromedriver.exe'}
    jpl_browser = mars_browser
    
    url = jpl_url
    jpl_browser.visit(url)
    
    html = jpl_browser.html
    soup = bs(html, 'html.parser')

    carousel_html = soup.find('div', 'carousel_items')
    feature_image = carousel_html.find('article alt')
    # images = 'https://www.jpl.nasa.gov' + relative_image_path

    # Store data in a dictionary
    # mars_pic = images

    # Close the browser after scraping
    jpl_browser.quit()
    
    # Code to get the Mars Facts
    mars_table = pd.read_html(mars_facts_url)
    mars_table = pd.read_html(mars_facts_url)
    mars_facts = pd.DataFrame(mars_table[0])
    mars_facts.columns=["Fact", "Value"]
    mars_facts.set_index(["Fact"])
    mars_facts_dict = mars_facts.to_dict('record')

    
    cerberus_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    schiaparelli_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    syrtis_major_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    valles_marineris_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    mars_hemi_images = {}
    
    cerberus = {'title': 'Cerberus', 'img_url': cerberus_url}
    syrtis_mjr = {'title': 'Syrtis Major', 'img_url': syrtis_major_url}
    vales_marineris = {'title': 'Valles Marineris', 'img_url': valles_marineris_url}
    schiaparelli = {'title': 'Schiaparelli', 'img_url': schiaparelli_url}

    mars_hemi_images['cerberus'] = cerberus
    mars_hemi_images['syrtis_mjr'] = syrtis_mjr
    mars_hemi_images['vales_marineris'] = vales_marineris
    mars_hemi_images['schiaparelli'] = schiaparelli

        
    #response = requests.get(nasa_url)
    #soup = (bs(response.text, 'lxml'))
    #nasa_title = soup.title.text
    #nasa_paragraphs = soup.find_all('p')
    #nasa_dict = {'title': nasa_title, 'article': nasa_paragraphs}
    #mars_facts.update(nasa_dict)

    
    mars_dict = {}
    mars_dict.update(mars_hemi_images)
    mars_dict['mars_facts_dict'] = mars_facts_dict
    return mars_dict
    
if __name__ == "__main__":
    app.run(debug=True)