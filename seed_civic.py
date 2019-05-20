import requests
from model import Artwork, Neighborhood, connect_to_db, db
from server import app

from sqlalchemy import func 
from geoalchemy2.shape import from_shape
from shapely.geometry import Point




def load_civic(): 
    """Load Civic data."""
    print("Civic Artwork")

    r = requests.get("https://data.sfgov.org/resource/7rjr-9n9w.json")
    civic = r.json()
    

    for item in civic: 

        try:
            title = item["display_title"]
            artist = item["artist"]
            creation_date = item["creation_date"]
            #location = from_shape(Point(float(item["point"].get("latitude",0)), float(item["point"].get("longitude",0)))),
            latitude = item.get("latitude", 0)
            longitude = item.get("longitude",0)
            medium = item["medium"]
            art_desc = item["facility"] + item["current_location"]
            hint = item["location_description"]
            
        except KeyError as error: 
            print("Key Error")

        art = Artwork(title = title,
                      artist = artist,
                      creation_date = creation_date,
                      #location = from_shape(Point(float(item["point"].get("latitude",0)), float(item["point"].get("longitude",0)))),
                      latitude = latitude,
                      longitude = longitude,
                      source = 'civic',
                      medium = medium,
                      art_desc = art_desc,
                      hint = hint)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()


################################################################################

def set_val_art_id():
    """Set value for the next art_id"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Artwork.art_id)).one()
    max_id = int(result[0])

    # Set the value for the next art_id to be max_id + 1
    query = "SELECT setval('artworks_art_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    
    connect_to_db(app)

    load_civic()
    set_val_art_id()