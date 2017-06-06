# app/admin/__init__.py

from flask import Blueprint

its = Blueprint('its', __name__)

from . import views