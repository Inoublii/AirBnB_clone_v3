#!/usr/bin/python3

"""
File index.py
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

"""
create a route
"""


@app_views.route('/status')
def status():
    """
    Return  json for route
    """
    return jsonify({"status": "OK"})

