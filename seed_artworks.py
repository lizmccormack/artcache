from sqlalchemy import func 
from geoalchemy2.shape import from_shape, to_shape 
from shapely.geometry import Point, asShape
from model import Artwork, Neighborhood, connect_to_db, db
import requests
from server import app



def map_neighborhood(point): 

    neighborhood_objects = db.session.query(Neighborhood).all()

    dictionary = {}
    for neighborhood_object in neighborhood_objects: 
        try:
            multipolygon = to_shape(neighborhood_object.neighborhood_geom)
        except AssertionError:
            print("assertion error")
        dictionary[neighborhood_object.neighborhood_id] = multipolygon

    for neighborhood_id, multipolygon in dictionary.items(): 
        if multipolygon.contains(point) == True: 
            return neighborhood_id
        else: 
            return 118



def load_oneper(map_neighborhood): 
    """Load Public 1% Artwork into database"""
    print("Public 1% Artwork")

    r = requests.get("https://data.sfgov.org/resource/cf6e-9e4j.json")
    one_per = r.json()

    for item in one_per: 
        
        try: 
            title = item["title"]
            artist = item["title"]
            artist_desc = item["artistlink"]
            location = from_shape(Point(float(item["the_geom"]["latitude"]), float(item["the_geom"]["longitude"])))
            neighborhood_id = map_neighborhood(Point(float(item["the_geom"]["latitude"]), float(item["the_geom"]["longitude"])))
            medium = item["medium"]
            art_desc = item["name"] + item["location"]
            hint = item["accessibil"]
        
        except KeyError as error: 
            print("Key Error")

        art = Artwork(title = title,
                      artist = artist,
                      artist_desc = artist_desc,
                      location = location,
                      source = 'public_oneper',
                      neighborhood_id = neighborhood_id,
                      medium = medium,
                      art_desc = art_desc,
                      hint = hint)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()




def load_civic(map_neighborhood): 
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


def load_graffiti(map_neighborhood):
    """Load Graffiti into database."""
    print("Graffiti")

    r = requests.get("https://data.sfgov.org/resource/vg6y-3pcr.json")
    graffiti = r.json()

    for item in graffiti:
        try:
            title = item['category'] 
            creation_date = item['opened']
            location = from_shape(Point(float(item['point']['latitude']),float(item['point']['longitude'])))
            source = 'graffiti'
            neighborhood_id = map_neighborhood(Point(float(item["the_geom"]["latitude"]), float(item["the_geom"]["longitude"])))
            art_desc = item["request_details"]
            hint = item["request_type"]
            img = item["media_url"]
        
        except KeyError as error:
            print("Key Error")

        art = Artwork(title = title,
                      location = location,
                      source = 'graffiti',
                      neighborhood_id = neighborhood_id,
                      medium = 'graffiti',
                      art_desc = art_desc,
                      hint = hint,
                      img = img)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()



if __name__ == "__main__":
    
    connect_to_db(app)


    load_oneper(map_neighborhood)




