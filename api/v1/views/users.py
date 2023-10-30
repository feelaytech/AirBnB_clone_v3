#!/usr/bin/python3
"""Defines URI routes for User objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User


@app_views.route("/users/", methods=["GET", "POST"])
def users_no_id(user_id=None):
    """Returns the list of all User objects and
       Creates a User object.
    """
    if request.method == "GET":
        all_users = storage.all("User")
        all_users = [obj.to_dict() for obj in all_users.values()]
        return jsonify(all_users)

    if request.method == "POST":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        if req_json.get("email") is None:
            abort(400, "Missing email")
        if req_json.get("password") is None:
            abort(400, "Missing password")
        new_object = User(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def user_with_id(user_id=None):
    """Returns a User object, Deletes a User object and
       Updates a User object, all by a given id.
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(user_obj.to_dict())

    if request.method == "DELETE":
        storage.delete(user_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        user_obj.base_model_abstract(req_json)
        return make_response(jsonify(user_obj.to_dict()), 200)
