from sqlalchemy import func 
from model import Artwork 
import requests





def load_oneper(): 
    """Load Public 1% Artwork into database"""
    print("Public 1% Artwork")

    r = requests.get("https://data.sfgov.org/resource/cf6e-9e4j.json")
    one_per = r.json()

    for item in one_per: 
        title= item["title"]
        artist= item["title"]
        artist_desc= item["artistlink"]
        creation_date = 
        location=(item["the_geom"]["latitude"], item["the_geom"]["longitude"])
        neighborhood_id= 
        medium=item["medium"]
        art_desc=item["name"] + item["location"]
        hint=item["accessibil"]

        art = Artwork(title=title,
                      artist=artist,
                      artist_desc=artist_link,
                      location=location,
                      source='public_oneper',
                      neighborhood_id=fill,
                      medium=medium,
                      art_desc=art_desc,
                      hint=hint)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()




def load_civic(): 
    """Load Civic Artwork into database."""
    print("Civic Artwork")

    r = requests.get("https://data.sfgov.org/resource/7rjr-9n9w.json")
    civic = r.json()

    for item in civic: 
        title= item["display_title"]
        artist= item["artist"]
        creation_date = item["creation_date"]
        location=(item["point"]["latitude"], item["point"]["longitude"])
        neighborhood_id= 
        medium=item["medium"]
        art_desc=item["name"] + item["location"]
        hint=item["location_description"]

        art = Artwork(title=title,
                      artist=artist,
                      creation_date=creation_date,
                      location=location,
                      location_geojson=fill,
                      source='civic',
                      neighborhood_id=fill,
                      medium=medium,
                      art_desc=art_dex,
                      hint=hint)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()


def load_graffiti():
    """Load Graffiti into database."""
    print("Graffiti")

    r = requests.get("https://data.sfgov.org/resource/vg6y-3pcr.json")
    graffiti = r.json()

    for item in graffiti:
        title
        artist 
        art_dec 
        creation_date
        location
        source
        neighborhood_id
        medium
        art_dec
        hint
        img

        art = Artwork(title=fill,
                  artist=fill,
                  artist_desc=fill,
                  location=fill,
                  location_geojson=fill,
                  source='graffiti',
                  neighborhood_id=fill,
                  medium=fill,
                  art_desc=fill,
                  hint=fill,
                  img=fill)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()



def load_neighborhood():
    """Load neighborhood data into database."""
    print("SF Neighborhoods")

    r = requests.get("https://data.sfgov.org/resource/6ia5-2f8k.json")
    neighborhoods = r.json()

    for item in neighborhoods:
        geom = item["the_geom"]
        name = item["name"]

        neighborhood = Neighborhoods(name=name,
                                     geom=geom)

        # add the data objects to the session
        db.session.add(neighborhood)

    # commit the changes to the db 
    db.session.commit()


