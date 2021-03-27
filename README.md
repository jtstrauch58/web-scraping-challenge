# Web-scraping-challenge


In this assignment, we are to build a web application that scrapes various websites for data related to the Mission to Mars and displays the information on a single HTML page.


## A brief overview of the assigment - information

### NASA Mars News

* Scrape https://mars.nasa.gov/news/ and collect the latest News Title and Paragraph Text.
* Assign the text to variables that you can reference later


### JPL Mars Space Images - Featured Image

* Use splinter to navigate https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html and find the image url for the current Featured Mars Image.

* Assign the url string to a variable


### Mars Facts

* Visit the Mars Facts webpage (https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

* Use Pandas to convert the data to a HTML table string.


### Mars Hemispheres

* Visit the USGS Astrogeology site (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

* Click each of the links to the hemispheres in order to find the image url to the full resolution image.

* Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.

* Append the dictionary with the image url string and the hemisphere title to a list.


## How the assignment was completed - jupyter notebook, flask, mongodb

* all scraping and dictionary assignment was completed in the jupyter notebook

* the jupyter notebook was converted to python script to make a scrape_mars.py with scrape function that returned a dictionary object

* use flask to create a home route '/' and '/scrape' route

* the '/scrape' route calls the scrape function in scrape_mars.py and exports the returned dictionary to mongoDB

* the '/' will find the correct data in the mongoDB and then render the index.html page

* an index.html page was generated (rendered) to display the mars information



