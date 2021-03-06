from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry        # imports geoalchemy2 for geoJSON fields 
from geoalchemy2.shape import from_shape, to_shape 
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# connection to the postgresql database through Flask-SQLAlchemy 
db = SQLAlchemy()

# Model definitions 

class Artwork(db.Model):
    """Artwork model."""

    __tablename__ = 'artworks' 
    
    art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    artist = db.Column(db.String(255))                                    
    artist_desc = db.Column(db.String(150))
    creation_date = db.Column(db.String(100))
    location = db.Column(Geometry('POINT'))                
    latitude =db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    source = db.Column(db.String(255), nullable=False)                      
    medium = db.Column(db.String(250))
    art_desc = db.Column(db.String(200))
    hint = db.Column(db.String(250), nullable=False)
    img_filename = db.Column(db.String(255)) 
    img_url = db.Column(db.String(255))


    def __repr__(self):
        """Create a readable data object for artworks objects."""
        return f'<Artwork art_id:{self.art_id}, artist{self.artist}, location: {self.location}>'

class User(db.Model):
    """User Model.""" 

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)     
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # # flash-login methods 
    def is_active(self):
        """Returns True, all users are active."""
        return True 

    def is_authenticated(self):
        """Returns True if the user is authenticated."""
        return self.authenticated
   
    def get_id(self): 
        """Identifies the user."""
        return self.email

    def check_password(self, password):
        """Check if the argument password matches user password."""
        return check_password_hash(self.password, password)

    def validate_email(self, email): 
        """Check if email is in users table."""
        
        user = User.query.filter_by(email=email).first()
        if user is not None: 
            raise ValidationError('Please use a different email address')

    def validate_username(self, username):
        """Check if username is in users table."""

        user = User.quer.filter_by(username=username).first()
        if user is not None:
            raise ValidationError('Please use a differnt username')

    def __repr__(self):
        """Create a readable data object for users objects."""
        return f'<User user_id:{self.user_id} email: {self.email}>'


class Add(db.Model):
    """Add model."""

    __tablename__ = "adds"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('artworks.art_id'), primary_key=True)
    date_time_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # relationship 
    user = db.relationship('User', backref='adds')
    artwork = db.relationship('Artwork', backref='adds')

    def __repr__(self):
        """Create a readable data object for adds objects."""
        return f'<Add user_id: {self.user_id} art_id: {self.art_id}>'


class Log(db.Model):
    """Log model."""

    __tablename__ = "logs"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('artworks.art_id'), primary_key=True)
    date_time_logged = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comment = db.Column(db.String(150))
    img = db.Column(db.String(50), nullable=False)                          

    # relationship 
    user = db.relationship('User', backref='logs')
    artwork = db.relationship('Artwork', backref='logs')


    def __repr__(self):
        """Create a readable data object for logs objects."""
        return f'<Log user_id: {self.user_id} art_id: {self.art_id}>'



class Neighborhood(db.Model):
    """Neighborhood model."""

    __tablename__ = "neighborhoods"

    neighborhood_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    neighborhood_geom = db.Column(Geometry('MULTIPOLYGON'))       


    def __repr__(self):
        """Create a readable data object for artworks objects."""
        return f'<Neighborhood neighborhood_id:{self.neighborhood_id} name:{self.name}>'


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    Add.query.delete()
    Log.query.delete()
    Artwork.query.delete()
    User.query.delete()

    leo = User(email='leonard@gmail.com', username='leo', password='artrules')
    liz = User(email='liz@gmail.com', username='liz', password='artrules2')

    db.session.add_all([leo, liz])
    db.session.commit()

################################################################################
# Helper functions 

def connect_to_db(app, db_uri="postgresql:///artcache"):
    """Connect the database to flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__": 

    from server import app
    connect_to_db(app)
    print("Connected to DB.")