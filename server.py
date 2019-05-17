from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session) 
from flask_debugtoolbar import DebugToolbarExtension
from model import Artwork, User, Add, Log, Neighborhood, connect_to_db, db



app = Flask(__name__)

# requires a secret key to use Flask session and debug toolbar 
app.secret_key ='12345'


# makes sure jinja fails loudly with an error 
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage route."""
    return render_template("homepage.html")

@app.route('/art/{id}')
def art_info():
    """Show Art Information"""
    return render_template("art_info.html")

@app.route('/art/{id}', methods=['POST'])
def add_art():
    """Add new art site."""
    pass

def login():
    """User login."""
    return render_template("login.html")












if __name__ == "__main__":
    # needs to be true for the debug toolbar 
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')