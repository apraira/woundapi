'''
from flask import(
    Blueprint, Response, flash, g, redirect, render_template, request, session, url_for, current_app, Markup, send_from_directory
)
import functools, logging, os, json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.db import delete_user, get_db, get_collection, get_pasien, get_user, get_users, insert_pasien, get_pasien_ns
from . import utils
from . import db
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List

bp = Blueprint('pasien', __name__, url_prefix='/')

#akses semua pasien
@bp.route('/pasien', methods =['GET'])
def get_pasiens():
    a = db.get_pasiens()
    print(a)
    return Response(response = json.dumps(list(a)), mimetype="application/json", status=200)

#mendaftarkan pasien baru
@bp.route('/pasien/<nrm>/<id_perawat>/<nama>/<usia>/<berat>/<tinggi>', methods=["POST"])
def create_pasien(nrm, id_perawat, nama, usia, berat,tinggi):
    try:
        filter = {}
        filter["_id"] = nrm
        filter["id_perawat"] = int(id_perawat)
        filter["nama"] = nama
        filter["usia"] = usia
        filter["berat"] = berat        
        filter["tinggi"] = tinggi
        cek = get_pasien(filter)

       
        if cek == None: 
            a = list(db.get_pasiens())

            data = {"_id": nrm,
                    "id_perawat": int(id_perawat),
                    "nama":nama,
                    "usia":usia,
                    "berat": berat,
                    "tinggi": tinggi}
            
            row = insert_pasien(data)
            print("berhasil input user baru")
            return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        else:
            #jika sudah ada data yang sama maka tidak bisa daftar lagi
            return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=404)

    except Exception as ex:
        print("Input user baru gagal")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

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
        '''