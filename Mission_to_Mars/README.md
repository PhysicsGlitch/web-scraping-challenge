This was a fun assignment that involved taking a number of webscraping utilities and then building them into a flask application.

The following repo contains the initial Jupyter Notebook files that were used to build the scraping functions and then the final python code and templates
that turned this scrape data into a Flask app using MongoDB.

In terms of the code, I commented the majority of my steps in the jupyter notebook to leave the app code cleaner. I employed Beautiful Soup, Splinter
and Pandas ability to read html tables to perform my scrapes. A few of the scrapes were trickier, especially getting NASA's featured image.

I had to find the carousel items and then created a regex search using the python re library in order to extract the image url. However, it did 
work in the end and the app updates the image everytime I run the code.

To move from my scrape_mars.py to my flask app I turned all of my data into a single dictionary. I then indexed this dictionary to the appropriate
elements in my html index file. I employed Bootswatch's darkly template to build the final website.