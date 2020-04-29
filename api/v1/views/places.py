#!/usr/bin/python3
"""
Define Place routes.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def places(city_id):
    """Define GET /cities/
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    user_id = doc.get('user_id')
    if user_id is None:
        return "Missing user_id", 400
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if doc.get('name') is None:
        return 'Missing name', 400
    doc["city_id"] = city_id
    place = Place(**doc)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def place_id(place_id):
    """Defines /places
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        return jsonify(place.to_dict())

    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({})

    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    for k, v in doc.items():
        if k not in ("id", "user_id", "city_id", "created_at", "updated_at"):
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())
