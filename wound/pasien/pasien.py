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
                    "id_perawat": request.form['id_perawat'],
                    "nama":request.form['nama'],
                    "agama":request.form['agama'],
                    "born_date":request.form['born_date'],
                    "usia":request.form['usia'],
                    "kelamin": request.form['kelamin'],
                    "alamat": request.form['alamat'],
                    "no_hp": request.form['no_hp'],
                    "email": request.form['email'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S")
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