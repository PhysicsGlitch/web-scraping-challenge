from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
mars_facts = mongo.db.mars_facts


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # I created an index for me mongodb beecause it was an easy collection method and also made it easy to reference
    # it in the html file
    mars_facts = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars_facts=mars_facts)

# Route that will trigger the scrape function

@app.route("/scrape")
def scraper():
    mars_facts_data = scrape_mars.scrape_mars_data()
    mongo.db.collection.update({}, mars_facts_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)