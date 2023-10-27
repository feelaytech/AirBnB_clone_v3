#!/usr/bin/python3
"""Defines URI routes for Review objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def reviews_per_place(place_id=None):
    """Returns the list of all Review objects of a Place,
       Creates a Review object, all by a given place id.
    """
    place_obj = storage.get(Place, place_id)

    if request.method == "GET":
        if place_obj is None:
            abort(404, "Not found")
        all_reviews = storage.all(Review)
        place_reviews = [obj.to_json() for obj in all_reviews.values()
                         if obj.place_id == place_id]
        return jsonify(place_reviews)

    if request.method == "POST":
        if place_obj is None:
            abort(404, "Not found")
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, "Missing user_id")
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404, "Not found")
        if req_json.get("text") is None:
            abort(400, "Missing text")
        review = storage.get(Review)
        req_json["place_id"] = place_id
        new_object = review(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_json()), 201)


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def reviews_with_id(review_id=None):
    """Returns a Review object, Deletes a Review object and
       Updates a Review object, all by a given review id.
    """
    review_obj = storage.get(Review, review_id)

    if request.method == "GET":
        if review_obj is None:
            abort(404, "Not found")
        return jsonify(review_obj.to_json())

    if request.method == "DELETE":
        if review_obj is None:
            abort(404, "Not found")
        review_obj.delete()
        del review_obj
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        if review_obj is None:
            abort(404, "Not found")
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        review_obj.bm_update(req_json)
        return make_response(jsonify(review_obj.to_json()), 200)
