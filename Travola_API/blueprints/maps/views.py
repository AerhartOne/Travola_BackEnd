from flask import Blueprint, url_for, request
from flask.json import jsonify
from models.trip_event import TripEvent
from app import geocoder
import textwrap

maps_api_blueprints = Blueprint('maps_api',
                                __name__,
                                template_folder='templates')

# @maps_api_blueprints.route('/')
# def home():
#     response = geocoder.forward("Next Academy")
#     response_status_code = response.status_code
#     response_headers = response.headers
#     collection = response.json()
#     collection['type'] == 'FeatureCollection'
#     # first = response.geojson()['features'][0]

#     # return render_template('home.html', first=first, collection=collection, response=response)
#     # return = jsonify({
#     #     'data': 
#     # })


@maps_api_blueprints.route('/search', methods=['POST'])
def map():
    query = request.form['location_search']
    response = geocoder.forward(query)
    first = response.geojson()['features'][0]
    latitude = response.geojson()['features'][0]['center'][0]
    longitude = response.geojson()['features'][0]['center'][1]
    truncated_address = textwrap.shorten(first['place_name'], width=60, placeholder="...")

    # return render_template('map.html', query=query, truncated_address=truncated_address, response=response, latitude=latitude, longitude=longitude, first=first, trips=trips)
    return jsonify({
        'latitude' : latitude,
        'longitude' : longitude,
        'address_short' : truncated_address
    })