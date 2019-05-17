from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session) 
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import func 
from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction
from geoalchemy2.shape import from_shape, to_shape 
from shapely.geometry import Point

from model import Artwork, User, Add, Log, Neighborhood, connect_to_db, db
import json
import googlemaps
import os

gmaps = googlemaps.Client(key=os.GOOGLE_MAPS_KEY)
app = Flask(__name__)

# requires a secret key to use Flask session and debug toolbar 
app.secret_key ='12345'


# makes sure jinja fails loudly with an error 
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def get_homepage():
    """Homepage route."""

    artworks = db.session.query(Artwork).all()

    
    # art_geojson = 
    #     { "type" : "Feature Collection",
    #         {"features" : [{
    #             "type": "Feature",
    #             "geometry": {
    #                 "type": "Point",
    #                 "coordinates": [artwork.latitude, artwork.longitude]
    #             },
    #             "properties": {
    #             "name": artwork.title
    #     }
    # }

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
    
    location = street_address + ',' + 'San Francisco' + 'CA'
    geocode_result = gmaps.geocode(location)
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']

    art = Artwork(title = title,
                  artist = artist,
                  artist_desc = art_desc,
                  location = from_shape(Point(latitude, longitude)),
                  latitude = latitude,
                  longitude = longitude,
                  source='user',
                  medium = medium,
                  art_desc = art_desc,
                  hint = hint)

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

if __name__ == "__main__":
    # needs to be true for the debug toolbar 
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')