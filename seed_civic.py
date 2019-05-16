from sqlalchemy import func 
from geoalchemy2.shape import from_shape, to_shape 
from shapely.geometry import Point, asShape
from model import Artwork, Neighborhood, connect_to_db, db
import requests
from server import app
from seed_artworks import map_neighborhood


def load_civic(function): 
    """Load Civic Artwork into database."""
    print("Civic Artwork")

    r = requests.get("https://data.sfgov.org/resource/7rjr-9n9w.json")
    civic = r.json()

    for item in civic: 
        try:
            title = item["display_title"]
            artist = item["artist"]
            creation_date = item["creation_date"]
            location = from_shape(Point(float(item["point"]["latitude"]), float(item["point"]["longitude"])))
            neighborhood_id = map_neighborhood(Point(float(item["the_geom"]["latitude"]), float(item["the_geom"]["longitude"])))
            medium = item["medium"]
            art_desc = item["name"] + item["location"]
            hint = item["location_description"]
        
        except KeyError as error: 
            print("Key Error")

        art = Artwork(title = title,
                      artist = artist,
                      creation_date = creation_date,
                      location = location,
                      source = 'civic',
                      neighborhood_id = neighborhood_id,
                      medium = medium,
                      art_desc = art_dex,
                      hint = hint)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()


if __name__ == "__main__":
    
    connect_to_db(app)


    load_civic(map_neighborhood)