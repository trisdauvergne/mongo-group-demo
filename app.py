from flask import Flask, render_template
import os
import env
import pymongo


app = Flask(__name__)


MONGO_URI = os.environ.get("MONGO_URI")     # What machine to speak to, who I am and my password (+ what database I want to deal with)
DBS_NAME = "test_database"                  # What database (a series of "tables")
COLLECTION_NAME = "movies"                  # What collection (what table)


@app.route("/")
def home():
    return render_template('hello.html')


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e

# REPRESENTS THE DATABASE SERVER
conn = mongo_connect(MONGO_URI)
# REPRESENTS THE COLLECTION
coll = conn[DBS_NAME][COLLECTION_NAME]


# CRUD - Create, Read, Update, Delete


# Create - inserting data into the database
@app.route("/create")
def create():
    my_wonderful_new_document = {'title': 'Jaws',
                                 'release_year': '1975',
                                 'synopsis': 'Another relaxing movie'}

    coll.insert_one(my_wonderful_new_document)

    return render_template('create.html', document=my_wonderful_new_document)

# Read - pulling data from the database
@app.route("/read")
def read():
    documents = coll.find()
    return render_template('read.html', documents=documents)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)