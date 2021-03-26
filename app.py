from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd

# create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    
    data_mars = mongo.db.data_mars.find_one()
    
    return render_template("index.html", data=data_mars)

@app.route("/scrape")
def scrape():
    
    data_mars = mongo.db.data_mars

    nasa_news = scrape_mars.scrape_info()

    mongo.db.data_mars.update({}, nasa_news, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

