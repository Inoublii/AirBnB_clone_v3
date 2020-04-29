#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify

"""
create a route
"""

@app_views.route('/status')
def status():
    """
    Return  json for route
    """
    my_dict = {'status': "OK"}
    return jsonify(my_dict)
