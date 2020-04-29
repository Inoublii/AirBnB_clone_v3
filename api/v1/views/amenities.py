#!/usr/bin/python3
"""Define Amenity Routes"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """Define GET /amenities
    """
    if request.method == "GET":
        return jsonify([amenity.to_dict()
                        for amenity in storage.all("Amenity").values()])

    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    if doc.get("name") is None:
        return "Missing name", 400
    amenity = Amenity(**doc)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def amenity_id(amenity_id):
    """

    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if request.method == "GET":
        return jsonify(amenity.to_dict())

    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    for k, v in doc.items():
        if k not in ("id", "created_at", "updated_at"):
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
