import functools, logging, os, json
import pprint
from flask import(
    Blueprint, Response, flash, g, redirect, render_template, request, session, url_for, current_app, Markup, send_from_directory
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.user.db import delete_user, get_db, get_collection, get_user, get_users, insert_user, update_user, get_nama_user
from wound import utils
from . import db
from flask import Flask, jsonify
from bson.objectid import ObjectId

bp = Blueprint('user', __name__, url_prefix='/')

#akses semua user / nurse
@bp.route('/user', methods =['GET'])
def get_users():
    a = db.get_users()
    return Response(response = json.dumps(list(a)), mimetype="application/json", status=200)

#post user / membuat user
@bp.route('/user/<name>/<username>/<email>/<passw>', methods=["POST"])
def create_user(name, username, email, passw):
    try:
        filter = {}
        filter["name"] = name
        filter["username"] = username
        filter["email"] = email
        filter["password"] = passw        
        cek = get_user(filter)

       
        if cek == None: 
            a = list(db.get_users())

            data = {"_id": 820000000 + len(a) + 1,
                    "name":name,
                    "username":username,
                    "email": email,
                    "password": passw}
            
            row = insert_user(data)
            print("berhasil input user baru")
            return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        else:
            #jika sudah ada data yang sama maka tidak bisa daftar lagi
            return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=404)

    except Exception as ex:
        print("Input user baru gagal")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

#cek user
@bp.route('/user/find/<username>/<passw>')
def find_user(username,passw):
    try:
        filter = {}
        filter["username"] = username
        filter["password"] = passw
        a = get_user(filter)
        if a == None:
            print(a)
            return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=404)
        else:
            print(a)
            return Response(response = json.dumps(dict(a)), mimetype="application/json", status=200)
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

#update data user
@bp.route('/user/update', methods =['POST'])
def update_perawat():

    id_perawat = request.form['id_perawat']
    jenis = request.form['jenis']
    isian = request.form['isian']

    filter = {}
    filter[jenis] = isian

    try:        
        update_user(id_perawat, filter)
        return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
    
            
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

#cek perawat berdasarkan id atau username
@bp.route('/user/<username>', methods =['GET'])
def cek_data_perawat(username):
    try:

        filter = {}
        filter2 = {}

        if username.isnumeric() == True:
            filter["_id"] = int(username)
        else:
            filter["_id"] = username        
        
        filter2["username"] = username

        teee = {"$or":[ filter, filter2]}

        cek = get_user(teee)
        test = dict(cek)

        result ={}
        result["_id"] = test["_id"]
        result["name"] = test["name"]
        result["username"] = test["username"]
        result ["email"] = test["email"]
        result["password"] = ""

       
        if cek == None:
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            print(cek)
            cek["password"] = ""
            return Response(response = json.dumps(cek), mimetype="application/json", status=200)

    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)


#upload gambar
@bp.route('/user/profile_img', methods =['POST'])
def post_user_image():
                 
    #next save the file
    
    file = request.files['image']
    id_perawat = request.form['id_perawat']

    

    try:
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = utils.pad_timestamp(filename)
            path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR']).replace("uploads","")
            fixed_path = os.path.join(path, "userImage")

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

            update_user(id_perawat, filter)           
              

            print(filepath)
            current_app.logger.debug(filepath);         
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)


"""#delete
@bp.route('/user/delete/<username>/<passw>', methods=["DELETE"])
def delete_user(username,passw):
    try:
        filter = {}
        filter["username"] = username
        filter["password"] = passw
        a = get_user(filter)
        if a == None:
            print(a)
            return Response(response = json.dumps({"message" : "user not found"}), mimetype="application/json", status=404)
        else:
            data = {}
            data["username"] = data
            delete_user(filter)
            return Response(response = json.dumps({"message" : f"data atas nama {username} sudah dihapus"}), mimetype="application/json", status=200)
    except Exception as ex:
        return Response(response = json.dumps({"error message": ex}), mimetype="application/json", status=500)"""




"""@bp.route('/admin_home')
def admin_home():
    name = g.user['name']    
    filter = {}
    filter['type'] = {'$exists': 0}
    doc = get_users(filter)
    count = doc.count()

    #query all users
    return render_template('admin_home.html', name = name, nuser = count, users = doc)


@bp.route('/create_admin/<email>/<passw>')
def create_admin(email, passw):
    #email = "semnasmath@unj.ac.id"
    data = {"email": email,
                "password": generate_password_hash(passw), 
                "name" : "Admin", 
                "type" : "master",                 
                }
    row = insert_user(data)
    flash("Admin " + email + " is created successfully") 
    return render_template('user_success.html')

@bp.route('/update_password/<email>/<passw>')
def update_password(email, passw):
    data = {
            "password": generate_password_hash(passw), 
            }

    # result = update_user({'_id': ObjectId(user_id)}, {'$set': data})
    result = update_user({'email': email}, {'$set': data})  
    flash("User " + email + " password has been updated")
    return render_template('user_success.html')"""


