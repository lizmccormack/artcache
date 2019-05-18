import requests
from model import Artwork, Neighborhood, connect_to_db, db
from server import app

from sqlalchemy import func 
from geoalchemy2.shape import from_shape
from shapely.geometry import Point




def load_oneper(): 
    """Load Public 1% Artwork into database"""
    print("Public 1% Artwork")

    r = requests.get("https://data.sfgov.org/resource/cf6e-9e4j.json")
    one_per = r.json()

    for item in one_per: 
        
        try: 
            art_title = item["title"].split(" by ")
            title = art_title[0]                       #to do: remove the '\' on either side of title
            artist = art_title[1]
            artist_desc = item["artistlink"]
            location = from_shape(Point(float(item["the_geom"]["latitude"]), float(item["the_geom"]["longitude"])))
            latitude=item["the_geom"]["latitude"]
            longitude=item["the_geom"]["longitude"]
            medium = item["medium"]
            art_desc = item["name"] + item["location"]
            hint = item["accessibil"]
        
        except KeyError as error: 
            print("Key Error")
        except IndexError as error:
            print("IndexError")

        art = Artwork(title = title,
                      artist = artist,
                      artist_desc = artist_desc,
                      location = location,
                      latitude = latitude,
                      longitude = longitude,
                      source = 'public_oneper', 
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

    load_oneper()
    set_val_art_id()





