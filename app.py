from flask import Flask, render_template, redirect, url_for
from flask_pymongo  import PyMongo
import mars_scraping

app = Flask(__name__)
#use flask pymongo to set up connection to database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():    
    #sccess info from db
    mars_data = mongo.db.marsData.find_one()
    print(mars_data)
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    #reference to database collectio (table)
    marsTable = mongo.db.marsData

    #drop table if it exists
    mongo.db.marsData.drop()


    #call mars scrapimh script
    mars_data = mars_scraping.scrape_all()
    
    #take dict and load into mongodb
    marsTable.insert_one(mars_data)

    #go back to index route

    return redirect("/")
  

if __name__ =="__main__":
    app.run()
