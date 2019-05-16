from sqlalchemy import func 
from model import Neighborhood
import requests



def load_neighborhood():
    """Load neighborhood data into database."""
    print("SF Neighborhoods")

    r = requests.get("https://data.sfgov.org/resource/6ia5-2f8k.json")
    neighborhoods = r.json()
    

    for item in neighborhoods:
        name = item["name"]
        geojson = str(item["the_geom"])
        geom = 

        #shapley: POLYGON(item['the_geom'][coordinates][0][0])
        #geom: use geo to_shape 

        #instanciate a neighboorhood and add coverted geom to column neighborhood_geom (in below)

        neighborhood = Neighborhood(name=name,
                                    neighborhood_geojson=geojson,
                                    neighborhood_geom=geom
                                    )

        # add the data objects to the session
        db.session.add(neighborhood)

    # commit the changes to the db 
    db.session.commit()


if __name__ == "__main__":
    
    connect_to_db(app)
