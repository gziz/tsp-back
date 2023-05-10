from flask import Blueprint,render_template,redirect,url_for, request, jsonify
from project import db
from project.models import Location, format_location
from tsp.tsp import tsp
import pandas as pd

locations_blueprint = Blueprint('locations', #2
                                __name__,
                                template_folder='templates/locations')


#GET ALL EVENTS
@locations_blueprint.route('/create_route', methods=['GET']) #1
def get_locations():
    try:
        locations = Location.query.all()
        locations = [format_location(loc) for loc in locations]
    except:
        locations = pd.read_csv('../data/cengage-fake.csv')
        locations = [format_location(loc) for idx, loc in locations.iterrows()]

    response = jsonify({'locations': locations})
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response


#CREATE OPTIMAL PATH
@locations_blueprint.route('/compute_route', methods=['POST']) ## 1
def compute_route():

    locations_ids = request.json['locations_id']
    locations = db.session.query(Location).filter(Location.id.in_(locations_ids))
    locations = [format_location(loc) for loc in locations]

    tour, tour_info = tsp(locations)

    response = jsonify({'tour': tour, "tour_info": tour_info})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#CREATE OPTIMAL PATH
@locations_blueprint.route('/show_route') 
def show_route():
    
    response = jsonify({'status': 200})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response