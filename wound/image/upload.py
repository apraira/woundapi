from flask import(
    Blueprint, Response, request)
import json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.pasien.helper import  get_pasien, insert_pasien, get_pasien_ns
from wound import utils
from wound import db
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List
import time
import functools, logging, os, json
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, Markup, send_from_directory
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId


bp = Blueprint('upload', __name__, url_prefix='/')

#upload gambar
@bp.route('/upload', methods =['POST'])
def post_image():
                 
    #next save the file
    file = request.files['image']  

    try:
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = utils.pad_timestamp(filename)
            path = os.path.join(current_app.config['UPLOAD_DIR'])
            try:
                os.makedirs(path)
            except OSError:
                pass
            filepath = os.path.join(path, filename)
            file.save(filepath)
            print(filepath)
            current_app.logger.debug(filepath);         
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)
        
    

#menampilkan gambar di web dulu
@bp.route('/search_image/<filename>', methods =['GET'])
def show_image(filename):
    path = os.path.join("\static\img")
    full_filename = os.path.join(path, filename)
    print(full_filename)
    return render_template("index.html", user_image = full_filename)