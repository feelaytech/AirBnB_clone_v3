#!/usr/bin/python3
"""Defines URI routes for State objects."""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET", "POST"])
def states():
    """Returns the list of all State objects
       and creates a State object as well.
    """
    if request.method == "GET":
        all_states = storage.all("State")
        all_states = list(obj.to_dict() for obj in all_states.values())
        return jsonify(all_states)
    if request.method == "POST":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        if req_json.get("name") is None:
            abort(400, "Missing name")
        new_object = State(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def states_with_id(state_id=None):
    """Returns a State object by a given id, deletes a State object
       by a given id and updates a State object by given id.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    if request.method == "GET":
        return jsonify(state_obj.to_dict())
    if request.method == "DELETE":
        storage.delete(state_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        req_json = request.get_json()
        if req_json is None:
            abort(400, "Not a JSON")
        state_obj.base_model_abstract(req_json)
        return jsonify(state_obj.to_dict())
