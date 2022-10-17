from uuid import uuid1
import numpy as np
import uuid
from flask import(
    Blueprint, Response, request)
import json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.image import helper
from wound.image.helper import get_images, image_list_by_id, insert_image, search_filename_from_id, update_image, get_image
from wound.pasien.helper import  get_pasien, insert_pasien, get_pasien_ns
from wound import utils
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
    id = uuid.uuid4().hex
    file = request.files['image']
    id_pasien = request.form['id_pasien']   

    try:
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = utils.pad_timestamp(filename)
            path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
            try:
                os.makedirs(path)
            except OSError:
                pass
            filepath = os.path.join(path, filename)
            file.save(filepath)
                       
            data = {"_id": id,
                    "id_pasien": id_pasien,
                    "id_perawat": request.form['id_perawat'],
                    "filename":filename,
                    "filepath":path,
                    "category":request.form['category'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    }
            insert_image(data)
            helper.update_image_user(id_pasien, id)  

            print(filepath)
            current_app.logger.debug(filepath);         
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)


#get all images data
@bp.route('/get_images', methods =['GET'])
def get_all_images():
    a = get_images()
    print(a)
    return Response(response = json.dumps(list(a)), mimetype="application/json", status=200)

#get 1 image berdasarkan id
@bp.route('/get_image/<id>', methods =['GET'])
def get_one_image(id):
    try:
        filter = {}
        filter["_id"] = id
        cek = get_image(filter)

       
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            print(cek)
            return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

    except Exception as ex:
        print("internal server error")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)


#delete 1 image berdasarkan id
@bp.route('/delete_image/<id>', methods= ['DELETE'])
def delete_image(id):
    ide = id
    helper.delete_one_image(ide)
    return Response(response = json.dumps({"message" : "1 image deleted"}), mimetype="application/json", status=200)

  
#download gambar tapi via image id
@bp.route('/get_image/<id>', methods =['GET'])
def show_image(id):
    filename = search_filename_from_id(id)
    path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
    return send_from_directory(path, filename, as_attachment=True)

#return image url via id
@bp.route('/get_image_url/<id>', methods = ['GET'])
def image_url(id):
    path = "https://jft.web.id/woundapi/instance/uploads/"
    filename = search_filename_from_id(id)
    img_url = path + filename
    return Response(response = json.dumps({"image_url" : img_url}), mimetype="application/json", status=200)

#return image url list via id pasien
@bp.route('/pasien_image_list/<id_pasien>', methods = ['GET'])
def image_url_list(id_pasien):
    img_url = []
    list = helper.pasien_image_list(id_pasien)
    path = "https://jft.web.id/woundapi/instance/uploads/"

    for i in list:
        filename = search_filename_from_id(i)
        img_url.append(path + filename)

    return Response(response = json.dumps({"image_url" : img_url}), mimetype="application/json", status=200)

#return image list via id pasien
#mendapatkan data pasien berdasarkan perawat yang mengurus
@bp.route('image/find/<id_pasien>')
def image_list_id(id_pasien):
    try:
        filter = {}
        filter["id_pasien"] = id_pasien
        data = {"id_pasien" : id_pasien}
        cek = image_list_by_id(data)

       
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            a = []
            for doc in cek:
                a.append(doc)

            print(a)
            return Response(response = json.dumps(a), mimetype="application/json", status=200)

    except Exception as ex:
        print(ex)
        print("internal server error")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)
