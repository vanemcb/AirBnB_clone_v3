#!/usr/bin/python3
""" Index module  """

from flask import Flask
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """ Method that returns the status """
    return ({"status": "OK"})
