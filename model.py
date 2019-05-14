from flask_sqlalchemy import SQLAlchemy 
from geoalchemy2 import Geometry        # imports geoalchemy2 for geoJSON fields 

# connection to the postgresql database through Flask-SQLAlchemy 
db = SQLAlchemy()


class Artwork(db.Model):
    """Artwork model."""

    __tablename__ = 'artworks'
    
    art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    artist = db.Column(db.String(50))                                    # nullable= true assumed - because some user entered artworks won't have artist 
    artist_desc = db.Column(db.String(150))
    location = db.Column(db.String(100), nullable=False)                  # can I store lat/lng tuple 
    location_geojson = db.Column(db.Geometry('POINT'), nullable=False)       # call using > geom = 'POINT(37 122)'
    source = db.Column(db.sting(10), nullable=False)                      # graffiti, one_per, civic, user
    neighborhood_id = db.Column(db.Integer, db.ForiegnKey('neighborhoods.neighborhood_id'), nullable=False)
    medium = db.Column(db.String(100))
    art_desc = db.Column(db.String(200))
    hint = db.Column(db.String(100), nullable=False)
    img = db.Column(db.string(50), nullable=False)  # is this the right datatpe? 

    # relationship syntatic sugar 
    neighborhood = db.relationship('Neighborhood', backref='artworks')

    def __repr__(self):
        """Create a readable data object for artworks objects."""
        return f'<Artwork art_id:{self.art_id}, artist{self.artist}, location: {self.location}>'


class User(db.Model):
    """User Model.""" 

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)     # need the user to have email, username and password 
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Create a readable data object for users objects."""
        return f'<User user_id:{self.user_id} email: {self.email}>'


class Add(db.Model):
    """Add model."""

    __tablename__ = "adds"

    user_id = db.Column(db.Integer, db.ForiegnKey('users.user_id'), nullable=False)
    art_id = db.Column(db.Integer, db.ForiegnKey('artworks.art_id'), nullable=False)
    date_time_added = db.Column(db.DateTime, nullable=False)

    # relationship syntactic sugar 
    user = db.relationship('User', backref='adds')
    artwork = db.relationship('Artwork', backref='adds')

    def __repr__(self):
        """Create a readable data object for adds objects."""
        return f'<Add user_id: {self.user_id} art_id: {self.art_id}>'


class Log(db.Model):
    """Log model."""

    __tablename__ = "logs"

    user_id = db.Column(db.Integer, db.ForiegnKey('users.user_id'))
    art_id = db.Column(db.Integer, db.ForiegnKey('artworks.art_id'))
    date_time_logged = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(150))
    img = db.Column(db.string(50), nullable=False)                           # filename string? 

    # relationship syntactic sugar 
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
    neighborhood_geom = db.Column(db.Geometry('MULTIPOLYGON'), nullable=False)


    def __repr__(self):
        """Create a readable data object for artworks objects."""
        return f'<Neighborhood neighborhood_id:{self.neighborhood_id} name:{self.name}>'




if __name__ == "__main__": 

    init_app()