from typing import Collection
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
def get_kajians(filter={}):
    collection = get_collection("kajian")
    return collection.find(filter)

#get data kajian by nrm pasien
def get_kajian_nrm(data):
    collection = get_collection("kajian")
    return collection.find(data)

#get 1 image
def get_kajian(filter={}):
    collection = get_collection("kajian")
    return collection.find_one(filter)

#tambah kajian baru
def insert_kajian(data):
    collection = get_collection("kajian")
    row = collection.insert_one(data)
    return row


#delete satu data kajian berdasarkan id
def delete_one_kajian(id):
    collection = get_collection("kajian")    
    return collection.delete_one({"_id":id})