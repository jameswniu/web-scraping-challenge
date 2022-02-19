import scrape_mars

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_info)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()

    mongo.db.mars_app.update({}, mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
