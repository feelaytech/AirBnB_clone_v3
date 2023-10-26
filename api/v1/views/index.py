#!/usr/bin/python3
"""Defines URI routes."""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """Returns the API status in a JSON format."""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Returns the number of each objects by type."""
    if request.method == "GET":
        resp = {}
        objs = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for k, v in objs.items():
            resp[v] = storage.count(k)
        return jsonify(resp)
