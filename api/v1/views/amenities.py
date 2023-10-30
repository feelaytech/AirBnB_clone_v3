#!/usr/bin/python3
"""Defines URI routes for Amenity objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage


@app_views.route("/amenities/", methods=["GET", "POST"])
def amenities_no_id(amenity_id=None):
    """Returns the list of all Amenity objects and
       creates an Amenity object.
    """
    if request.method == "GET":
        all_amenities = storage.all("Amenity")
        all_amenities = [obj.to_dict() for obj in all_amenities.values()]
        return jsonify(all_amenities)

    if request.method == "POST":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        if req_json.get("name") is None:
            abort(400, "Missing name")
        amenity = storage.get("Amenity")
        new_object = amenity(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def amenities_with_id(amenity_id=None):
    """Returns an Amenity object, Deletes an Amenity object and
       Updates an Amenity object, all by a given id.
    """
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(amenity_obj.to_dict())

    if request.method == "DELETE":
        storage.delete(amenity_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        amenity_obj.base_model_abstract(req_json)
        return make_response(jsonify(amenity_obj.to_dict()), 200)
