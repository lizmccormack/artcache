from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session, url_for, flash) 
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import func 
from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction
from geoalchemy2.shape import from_shape, to_shape 
from shapely.geometry import Point

from model import Artwork, User, Add, Log, Neighborhood, connect_to_db, db 
import os
import json
import googlemaps
from datetime import datetime
from flask import jsonify
import time
import boto3 
from PIL import Image 
import io

# flask-upload constants  
UPLOAD_FOLDER = 'static/image_uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# implement API key from secrets file 
gmaps = googlemaps.Client(os.environ['GOOGLE_MAPS'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

login_manager = LoginManager() #creates
login_manager.init_app(app)
login_manager.login_view = 'login'

# requires a secret key to use Flask session and debug tool bar 
app.secret_key ='12345'

# makes sure jinja fails loudly with an error 
app.jinja_env.undefined = StrictUndefined

# set up s3 client 
s3_resource= boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-west-2')
bucket_name = 'artcache'


@login_manager.user_loader
def load_user(email):

    return User.query.filter_by(email = email).first()


@app.route('/')
def get_homepage():
    """Homepage route."""

    return render_template("homepage.html")

@app.route('/art_tour')
def get_tour():
    """tour of SF."""

    return render_template("tour.html")


@app.route('/profile')
@login_required
def get_profile():
    """Profile route."""
    
    return render_template("profile.html")

@app.route('/logs.json')
def get_profile_logs():
    """User logs json for profile page"""

    user = db.session.query(User).filter(User.user_id == current_user.user_id).first()

    log_list = []
    for log in user.logs: 
        log_json = {
            "image": presigned_url(log.img),
            "comment": log.comment
        }
        log_list.append(log_json)

    user_log = {"username": current_user.username,
                "logs": log_list}

    return jsonify(user_log)

@app.route('/adds.json')
def get_profile_adds(): 
    """User adds json for profile page."""
    
    user = db.session.query(User).filter(User.user_id == current_user.user_id).first()

    add_list = []
    for add in user.adds: 
        add_json = {
            "title": add.artwork.title,
            "hint": add.artwork.hint,
            "image": presigned_url(add.artwork.img_filename),
        }
        add_list.append(add_json)

    user_add = {"username": current_user.username,
                "logs": add_list}

    return jsonify(user_add)

@app.route('/art_logs/<art_id>')
def get_art_logs(art_id):
    """Art specific logs for sidebar."""

    logs = db.session.query(Log).filter(Log.art_id == art_id).all()

    log_list = []
    for log in logs: 
        log_json = {
            "image": presigned_url(log.img),
            "comment": log.comment
        }
        log_list.append(log_json)

    art_log = {"username": current_user.username,
               "logs": log_list}

    return jsonify(art_log)


@app.route('/art/<art_id>', methods=['GET'])
def info_art(art_id):
    """Show information about art."""

    art = db.session.query(Artwork).filter(Artwork.art_id == art_id).one()

    return jsonify(title=art.title,
                   artist=art.artist,
                   hint=art.hint, 
                   art_id=art_id,
                   img = art.img_url)

@app.route('/log/<art_id>', methods=['POST'])
def log_art(art_id):
    """log page for art"""

    file = request.files['image']
    image_resize = process_image(file)
    img_filename = handle_img_upload(file)
    comment = request.form["comment"]

    time.sleep(2)

    print("NEW ORDER!!!!!!")

    log = Log(art_id=art_id,
              user_id = current_user.user_id,
              comment=comment,
              img=img_filename) 
    
    db.session.add(log)
    db.session.commit()

    s3_resource.put_object(Bucket=bucket_name, Key=img_filename, Body=image_resize)

    return "Your site had been logged"



@app.route('/artworks.json')
def get_artworks_json():
    """Return JSON object of all artworks in the database."""

    artworks = db.session.query(Artwork).all()

    body_list = []
    for artwork in artworks: 
        artwork_geojson = {"type":"Feature",
                           "properties":{"title": artwork.title, 
                                         "artist": artwork.artist, 
                                        "source":artwork.source, 
                                        "art_id": artwork.art_id, 
                                        "hint": artwork.hint},"geometry":{"type":"Point","coordinates":[artwork.longitude,artwork.latitude]}}
        body_list.append(artwork_geojson)

    geojson_result ={
        "type":"FeatureCollection",
        "features": body_list
        }

    return jsonify(geojson_result)

# @app.route('/neighborhoods.json')
# def get_neighborhoods_json():
#     """Return JSON object of all neighborhoods in database."""

#     neighborhoods = db.session.query(ST_AsGeoJSON(neighborhood_geom)).all()




@app.route('/add_art', methods=['GET', 'POST'])
@login_required
def add_art():
    """Add new art site."""

    if request.method == 'POST':

        # add new art! 
        title = request.form['title']
        artist = request.form['artist']
        artist_desc = request.form['artist_desc']
        address = request.form['address']
        medium = request.form['medium']
        art_desc = request.form['medium']
        hint = request.form['hint']
        latitude = geocode(address)[0]['geometry']['location']['lat']
        longitude = geocode(address)[0]['geometry']['location']['lng']
        file = request.files['image']
        image_resize = process_image(file)
        img_filename = handle_img_upload(file)

        # create art instance 
        art = Artwork(title = title,
                      artist = artist,
                      artist_desc = art_desc,
                      location = from_shape(Point(latitude, longitude)),
                      latitude = latitude,
                      longitude = longitude,
                      source='user',
                      medium = medium,
                      art_desc = art_desc,
                      hint = hint,
                      img_filename=img_filename)

        # add art to database 
        db.session.add(art)
        db.session.commit()


        # add to the add table 
        add = Add(user_id=current_user.user_id, 
                  art_id=art.art_id)

        db.session.add(add)
        db.session.commit()

        s3_resource.put_object(Bucket=bucket_name, Key=img_filename, Body=image_resize)

        return redirect('/')

    return render_template('add_art.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user_process():
    """Process user registration."""

    if request.method == 'POST': 

        # get information from registration from 
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = db.session.query(User).filter(User.email == email).first()

        # check for user 
        if not user: 
            # create a user instance 
            user = User(email=email,
                        username=username,
                        password=generate_password_hash(password)
                        )

            # add user to database 
            db.session.add(user)
            db.session.commit()

            flash('Thanks for registering, please login.')
            return redirect('/login')


        flash('You are already registered!')
        return redirect('/login')

    # if method is get, show register form 
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']

        user = db.session.query(User).filter_by(email = email).first()

        if not user or not user.check_password(password):
            
            flash('Please check your login details!')
            return redirect('/login')

        user.is_authenticated = True 
        login_user(user)
        return redirect('/')

    return render_template("login.html")


@app.route('/logout')
def logout():
    """User logout."""

    logout_user()
    return redirect('/')


# Helper Functions 

def allowed_file(filename):
    """Check for allowed file types in image upload."""

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def geocode(location):
    """geocode an address into lat/lng."""

    return gmaps.geocode(location)

def handle_img_upload(file):
    """check for image and create filepath to store in db."""

    if file.filename == '':
        flash('No file selected for uploading')
        return redirect('/add_art')
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        return filename 


def presigned_url(key, bucket=bucket_name, expiration=3600): 
    """Generate a presigned url for s3."""
    url = s3_resource.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket,
                                                        'Key': key},
                                                ExpiresIn=expiration)
    return url

def process_image(file):
    """resize images to thumbnails."""

    image = Image.open(file)
    image.thumbnail([200, 200],Image.ANTIALIAS)
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format='JPEG')
    image_resize = in_mem_file.getvalue()
    return image_resize


if __name__ == "__main__":
    # needs to be true for the debug tool bar 
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



