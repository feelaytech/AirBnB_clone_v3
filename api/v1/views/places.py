#!/usr/bin/python3
"""Defines URI routes for Place objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place
from models.city import City


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
        place_obj.bm_update(req_json)
        return make_response(jsonify(place_obj.to_dict()), 200)
