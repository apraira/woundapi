import os
from flask import(
    Blueprint, Response, current_app, request)
import json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.data_kajian.helper import update_id_pasien_kajian
from wound.image.helper import update_id_pasien_image
from wound.pasien.helper import  delete_one_pasien, get_pasien, insert_pasien, get_pasien_ns, update_id, update_pasien_new
from wound import utils
from wound import db
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List
import time


bp = Blueprint('pasien', __name__, url_prefix='/')

#akses semua pasien
@bp.route('/pasien', methods =['GET'])
def get_pasiens():
    a = db.get_pasiens()
    print(a)
    return Response(response = json.dumps(list(a)), mimetype="application/json", status=200)

#add pasien baru
@bp.route('/pasien', methods =['POST'])
def addpasien():
    try:        
            data = {"_id": request.form['_id'],
                    "id_perawat": int(request.form['id_perawat']),
                    "nama":request.form['nama'],
                    "agama":request.form['agama'],
                    "born_date":request.form['born_date'],
                    "usia":request.form['usia'],
                    "kelamin": request.form['kelamin'],
                    "alamat": request.form['alamat'],
                    "no_hp": request.form['no_hp'],
                    "email": request.form['email'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "list_image_id": []
                    }

            cek = get_pasien(data)
       
            if cek == None:
                row = insert_pasien(data)
                print("berhasil input user baru")
                return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
            
            else:
                #jika sudah ada data yang sama maka tidak bisa daftar lagi
                return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=404)                    
                            
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "exe"}), mimetype="application/json", status=500)


#mendapatkan data pasien berdasarkan id/nrm
@bp.route('/pasien/<nrm>', methods =['GET'])
def cek_data_pasien(nrm):
    try:
        filter = {}
        filter["_id"] = nrm
        cek = get_pasien(filter)

       
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            print(cek)
            return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

    except Exception as ex:
        print("internal server error")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

#delete 1 pasien berdasarkan id
@bp.route('/pasien/<id>', methods= ['DELETE'])
def delete_pasien(id):
    ide = id
    filter = {}
    filter["_id"] = ide
    cek = get_pasien(filter)
    delete_one_pasien(ide)
    return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

#mendapatkan data pasien berdasarkan perawat yang mengurus
@bp.route('pasien/find/perawat/<id_perawat>')
def cek_data_perawat_pasien(id_perawat):
    try:
        filter = {}
        filter["id_perawat"] = int(id_perawat)
        data = {"id_perawat" : int(id_perawat)}
        cek = get_pasien_ns(data)

       
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

#update data user
@bp.route('/pasien/update', methods =['POST'])
def update_data_pasien():

    id_perawat = request.form['id_pasien']
    jenis = request.form['jenis']
    isian = request.form['isian']

    if jenis == "_id":
        try:
            update_id(id_perawat,isian)
            update_id_pasien_kajian(id_perawat,isian)
            update_id_pasien_image(id_perawat,isian)
            return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
        except Exception as ex:
            print(ex)
            return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)
    else:
        filter = {}
        filter[jenis] = isian

        try:        
            update_pasien_new(id_perawat, filter)
            return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
        
                
        except Exception as ex:
            print (ex)
            return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)


#upload gambar
@bp.route('/pasien/profile_img', methods =['POST'])
def post_pasien_image():
                 
    #next save the file
    
    file = request.files['image']
    id_perawat = request.form['id_pasien']

    filter = {}
    filter["_id"] = id_perawat
    cek = get_pasien(filter)

    

    try:
        if file and utils.allowed_file(file.filename):

            
            filename = secure_filename(file.filename)
            filename = utils.pad_timestamp(filename)
            path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR']).replace("uploads","")
            fixed_path = os.path.join(path, "userImage")

            try:
                if cek["profile_image_url"] != None:
                    old_filename = cek["profile_image_url"].replace("https://jft.web.id/woundapi/instance/userImage/", "")
                    old_filepath = os.path.join(fixed_path, old_filename)
                    os.remove(old_filepath)
                else :
                    pass
            except Exception as ex:
                print (ex)

            filter = {}
            filter["profile_image_url"] = "https://jft.web.id/woundapi/instance/userImage/" + filename

            try:
                os.makedirs(fixed_path)
            except OSError:
                pass
            filepath = os.path.join(fixed_path, filename)
            file.save(filepath)
                       
            filter = {}
            filter["profile_image_url"] = "https://jft.web.id/woundapi/instance/userImage/" + filename

            update_pasien_new(id_perawat, filter)           
              

            print(filepath)
            current_app.logger.debug(filepath);         
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)

