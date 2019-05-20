from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry        # imports geoalchemy2 for geoJSON fields 
from geoalchemy2.shape import from_shape, to_shape 

# connection to the postgresql database through Flask-SQLAlchemy 
db = SQLAlchemy()


################################################################################
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
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Create a readable data object for users objects."""
        return f'<User user_id:{self.user_id} email: {self.email}>'


class Add(db.Model):
    """Add model."""

    __tablename__ = "adds"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('artworks.art_id'), primary_key=True)
    date_time_added = db.Column(db.DateTime, nullable=False)

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
    date_time_logged = db.Column(db.DateTime, nullable=False)
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





################################################################################
# Helper functions 

def connect_to_db(app):
    """Connect the database to flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///artcache'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__": 

    from server import app
    connect_to_db(app)
    print("Connected to DB.")