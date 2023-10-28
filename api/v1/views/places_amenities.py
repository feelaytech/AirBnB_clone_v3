#!/usr/bin/python3
"""Defines URI routes for link between Place-Amenity objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def amenities_per_place(place_id=None):
    """Returns the list of all Amenity objects of a Place
       by a given place id.
    """
    place_obj = storage.get(Place, place_id)

    if request.method == "GET":
        if place_obj is None:
            abort(404, "Not found")
        all_amenities = storage.all(Amenity)
        if storage_t == "db":
            place_amenities = place_obj.amenities
        else:
            place_amen_ids = place_obj.amenities
            place_amenities = []
            for am in place_amen_ids:
                response.append(storage.get(Amenity, am))
        place_amenities = [
            obj.to_dict() for obj in place_amenities
            ]
        return jsonify(place_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"])
def amenity_to_place(place_id=None, amenity_id=None):
    """Deletes an Amenity object to a Place,
       Links an Amenity object to a Place, all by a given Amenity id.
    """
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place_obj is None:
        abort(404, "Not found")
    if amenity_obj is None:
        abort(404, "Not found")

    if request.method == "DELETE":
        if (amenity_obj not in place_obj.amenities and
                amenity_obj.id not in place_obj.amenities):
            abort(404, "Not found")
        if storage_t == "db":
            place_obj.amenities.remove(amenity_obj)
        else:
            place_obj.amenity_ids.pop(amenity_obj.id, None)
        place_obj.save()
        return make_response(jsonify({}), 200)

    if request.method == "POST":
        if (amenity_obj in place_obj.amenities or
                amenity_obj.id in place_obj.amenities):
            return make_response(jsonify(amenity_obj.to_dict()), 200)
        if storage_t == "db":
            place_obj.amenities.append(amenity_obj)
        else:
            place_obj.amenities = amenity_obj
        return make_response(jsonify(amenity_obj.to_dict()), 201)
