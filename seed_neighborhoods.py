import requests
import json
from server import app

from sqlalchemy import func 
from geoalchemy2.shape import from_shape 
from model import Neighborhood, connect_to_db, db
import json
from shapely.geometry import shape
import shapely.wkb
import shapely.wkt



def load_neighborhood():
    """Load neighborhood data into database."""
    print("SF Neighborhoods")

    # requests data from SFData 
    r = requests.get("https://data.sfgov.org/resource/6ia5-2f8k.json")
    neighborhoods = r.json()
    

    for item in neighborhoods:
        
        name = item["name"]
        geojson = str(item["the_geom"]).replace("'", '"')
        geom = from_shape(shape(json.loads(geojson)))     # json.loads() loads a geojson string into a python object, shape turns it into a shapely feature, from shape turns it into a geom 
        neighborhood = Neighborhood(name=name,
                                    neighborhood_geom=geom)

        # add the data objects to the session
        db.session.add(neighborhood)

    # commit the changes to the db 
    db.session.commit()




if __name__ == "__main__":
    
    connect_to_db(app)

    load_neighborhood()