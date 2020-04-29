#!/usr/bin/python3
"""Define Review Routes"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def reviews(place_id):
    """

    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        return jsonify([review.to_dict() for review in place.reviews])

    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400

    user_id = doc.get("user_id")
    if user_id is None:
        return "Missing user_id", 400

    if storage.get("User", user_id) is None:
        abort(404)

    if doc.get("text") is None:
        return "Missing text", 400
    doc["place_id"] = place_id
    review = Review(**doc)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def review(review_id):
    """Define/reviews/<review_id>
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())

    elif request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})

    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    for k, v in doc.items():
        if k not in ("id", "user_id", "place_id", "created_at", "updated_at"):
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict())
