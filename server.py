from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session, url_for, flash) 
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename

from sqlalchemy import func 
from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction
from geoalchemy2.shape import from_shape, to_shape 
from shapely.geometry import Point

from model import Artwork, User, Add, Log, Neighborhood, connect_to_db, db
import os
import json
import googlemaps


# flask-upload constants  
UPLOAD_FOLDER = 'static/image_uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# implement API key from secrets file 
gmaps = googlemaps.Client(os.environ['GOOGLE_MAPS'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

# requires a secret key to use Flask session and debug toolbar 
app.secret_key ='12345'

# makes sure jinja fails loudly with an error 
app.jinja_env.undefined = StrictUndefined


################################################################################

@app.route('/')
def get_homepage():
    """Homepage route."""

    #artworks = db.session.query(Artwork).all()

    return render_template("homepage.html")


@app.route('/add_art', methods=['GET'])
def add_art_form():
    """Shows form for adding art"""
    return render_template('add_art.html')


@app.route('/add_art', methods=['POST'])
def add_art():
    """Add new art site."""

    title = request.form['title']
    artist = request.form['artist']
    artist_desc = request.form['artist_desc']
    street_address = request.form['street']
    medium = request.form['medium']
    art_desc = request.form['medium']
    hint = request.form['hint']
    
    # geocoding
    location = street_address + ',' + 'San Francisco' + 'CA' + 'USA'
    geocode_result = gmaps.geocode(location)
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']

    # image upload 
    file = request.files['image']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect('/add_art')
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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
                  img_filename=filename,
                  img_url=os.path.join(app.config['UPLOAD_FOLDER'], filename))


    db.session.add(art)
    db.session.commit()

    return redirect('/')


@app.route('/art/{id}')
def get_art_info():
    """Show Art Information"""
    return render_template("art_info.html")

@app.route('/register')
def register_user(): 
    """Register a user."""
    pass

@app.route('/login')
def login_user():
    """User login."""
    return render_template("login.html")


################################################################################
# Helper Functions 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    # needs to be true for the debug toolbar 
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')