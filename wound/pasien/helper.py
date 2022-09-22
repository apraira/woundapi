import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext

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

def get_pasiens(filter={}):
    collection = get_collection("pasien")
    return collection.find(filter)

def get_pasien_ns(data):
    collection = get_collection("pasien")
    return collection.find(data)

def get_pasien(filter={}):
    collection = get_collection("pasien")
    return collection.find_one(filter)

def insert_pasien(data):
    collection = get_collection("pasien")
    row = collection.insert_one(data)
    return row

def update_pasien(filter, update):
    collection = get_collection("pasien")    
    return collection.update_one(filter, update, upsert=False)

def delete_pasien(data):
    collection = get_collection("pasien")
    collection.delete_one(data)