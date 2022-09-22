import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
import gridfs

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]


#data pasien query
#fungsi khusus untuk  mencari data yang berhubungan dengan pasien

def get_images(filter={}):
    collection = get_collection("image")
    return collection.find(filter)
