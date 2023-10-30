#!/usr/bin/python3
"""Defines URI routes for City objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def cities_per_state(state_id=None):
    """Returns the list of all City objects of a State by state id,
       Creates a City object in a State id'd by state id.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)

    if request.method == "GET":
        all_cities = storage.all("City")
        state_cities = [obj.to_dict() for obj in all_cities.values()
                        if obj.state_id == state_id]
        return jsonify(state_cities)

    if request.method == "POST":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        if req_json.get("name") is None:
            abort(400, "Missing name")
        req_json["state_id"] = state_id
        new_object = City(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def cities_with_id(city_id=None):
    """Returns a City object, Deletes a City object and Updates a city object
       all by a given city id.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(city_obj.to_dict())

    if request.method == "DELETE":
        storage.delete(city_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        city_obj.base_model_abstract(req_json)
        return make_response(jsonify(city_obj.to_dict()), 200)
