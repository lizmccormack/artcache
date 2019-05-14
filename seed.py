from sqlalchemy import func 
from model import Artwork 


def delete_all():
    """function to delete everything before seeding."""
    Artwork.query.delete()


def load_oneper():
    """Load Public 1% Artwork into database"""
    print("Public 1% Artwork") # I don't want to delete the rows because adding three to a different database 

    # read file and insert data 
    for row in open("seed_data/one.art"): # what kind of datafile does this need to be 
        row = row.strip()
        
        name, 
        title, 
        type, 
        medium, 
        location, 
        accessible, 
        requiredAr, 
        description, 
        artist_link, 
        geom, 
        supervisor_districts, 
        fire_prevention_districts, 
        current_police_districts, 
        neighborhood_analysis_boundaries, 
        zip_codes = row.split(",")

        art = Artwork(title=fill,
                      artist=fill,
                      artist_desc=fill,
                      location=fill,
                      location_geojson=fill,
                      source=fill_static,
                      neighborhood_id=fill,
                      medium=fill,
                      art_desc=fill,
                      hint=fill,
                      img=fill)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()


def load_civic(): 
    """Load Civic Artwork into database."""
    print("Civic Artwork")

    # read file and insert data 
    for row in open("seed_data/civic"):
        row = row.strip()

        creation_data, 
        accession_number,
        artist,
        credit_line,
        display_title,
        display_dimensions,
        medium,
        media_support,
        facility,
        current_location,
        location_desc,
        street_address,
        street_address_2,
        district_name,
        geocoding_source,
        geocoding_accuracy, 
        geocoding_accuracy_type,
        latitude,
        longitude,
        point,
        sf_find_neighborhoods,
        current_police_districts,
        current_supervisior_districts = row.split(",")

        art = Artwork(title=fill,
                      artist=fill,
                      artist_desc=fill,
                      location=fill,
                      location_geojson=fill,
                      source=fill_static,
                      neighborhood_id=fill,
                      medium=fill,
                      art_desc=fill,
                      hint=fill,
                      img=fill)

        # add the data objects to the session
        db.session.add(art)

    # commit the changes to the db 
    db.session.commit()


