#!/usr/bin/python3
"""Defines URI routes for Place objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def places_per_city(city_id=None):
    """Returns the list of all Place objects of a City and
       Creates a Place, all by using a given city id.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        all_places = storage.all(Place)
        city_places = [obj.to_dict() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == "POST":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, "Missing user_id")
        user_obj = storage.get("User", user_id)
        if user_obj is None:
            abort(404, "Not found")
        if req_json.get("name") is None:
            abort(400, "Missing name")
        place = storage.get(Place)
        req_json["city_id"] = city_id
        new_object = place(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def places_with_id(place_id=None):
    """Returns a Place object, Deletes a Place object and
       Updates a Place object, all by a given place id.
    """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(place_obj.to_dict())

    if request.method == "DELETE":
        place_obj.delete()
        del place_obj
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        place_obj.base_model_abstract(req_json)
        return make_response(jsonify(place_obj.to_dict()), 200)


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """Endpoint to retrieve all Place objects
       depending on the JSON in the body of the request.
    """
    all_places = [p for p in storage.all(Place).values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    states = req_json.get("states")
    if states and len(states) > 0:
        all_cities = storage.all(City)
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get("cities")
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get(City, c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get("amenities")
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get(Amenity, a_id)])
        for p in all_places:
            p_amenities = None
            if storage_t == "db" and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
