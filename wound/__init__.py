import os
from flask import(
    Blueprint, Response, redirect, request)
from flask import Flask, jsonify, render_template
from wound.user import db
from . import submission
from wound.user import user
from wound.pasien import pasien
from wound.image import upload
from wound.data_kajian import datakajian
from wound.logging import logactivity

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.cfg', silent=True)
    
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(submission.bp)    
    app.register_blueprint(user.bp)
    app.register_blueprint(pasien.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(datakajian.bp)
    app.register_blueprint(logactivity.bp)

    ####routing

    """@app.before_request
    def before_request():
        if request.is_secure:
            url = request.url.replace('https://', 'http://', 1)
            code = 301
            return redirect(url, code=code)"""

    @app.route('/index')
    @app.route('/')
    def index():
        your_list= [1,2,3,4]
        return render_template('index.html', navigation=your_list)

    @app.route('/test', methods = ["POST"])
    def post_user():
        return "testing"

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    return app 

    
