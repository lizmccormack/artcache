from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session, url_for, flash) 
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, IMAGES, configure_uploads
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

# requires a secret key to use Flask session and debug toolbar 
app.secret_key ='12345'

# makes sure jinja fails loudly with an error 
app.jinja_env.undefined = StrictUndefined


@login_manager.user_loader
def load_user(email):

    return User.query.filter_by(email = email).first()


@app.route('/')
def get_homepage():
    """Homepage route."""

    return render_template("homepage.html")


@app.route('/profile')
@login_required
def get_profile():
    """Profile Page."""

    user_adds = db.session.query(Add).filter_by(Add.user_id == current_user.user_id).all()
    user_logs = db.session.query(Log).filter_by(Log.user_id == current_user.user_id).all()

    return render_template("profile.html", 
                           name=current_user.username, 
                           id=current_user.user_id,
                           user_adds=user_adds,
                           user_logs=user_logs)


@app.route('/artworks.geojson')
def get_artworks_json():
    """Return JSON object of all artworks in the database."""

    artworks = db.session.query(Artwork).all()

    body_list = []
    for artwork in artworks: 
        artwork_geojson = {"type":"Feature","properties":{"title": artwork.title, "artist": artwork.artist, "source":artwork.source, "art_id": artwork.art_id, "hint": artwork.hint},"geometry":{"type":"Point","coordinates":[artwork.longitude,artwork.latitude]}}
        body_list.append(artwork_geojson)

    geojson_result ={
        "type":"FeatureCollection",
        "features": body_list
        }

    return jsonify(geojson_result)


@app.route('/add_art', methods=['GET', 'POST'])
@login_required
def add_art():
    """Add new art site."""

    if request.method == 'POST':

        # add new art! 
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
        #neighborhood = geocode_result[0]['address_components'][1]['long_name']

        # image upload 
        file = request.files['image']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect('/add_art')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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
                      img_filename=filename,
                      img_url=os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # add art to database 
        db.session.add(art)
        db.session.commit()


        # add to the add table 
        add = Add(user_id=current_user.user_id, 
                  art_id=art.art_id)

        db.session.add(add)
        db.session.commit()

        return redirect('/')

    return render_template('add_art.html')

# DO THIS IN AJAX/JQUERY if possible 
@app.route('/art/<art_id>', methods=['GET', 'POST'])
def info_art(art_id):
    """show information about art.

    use this route for both the display of art 
    """

    art = db.session.query(Artwork).filter(Artwork.art_id == art_id).first()

    return render_template('info_art.html', art=art)




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


        flash('You are already registered! ')
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
    """Check for allowed filetypes in image upload."""
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