# app/admin/__init__.py

from flask import Blueprint

its = Blueprint('admin', __name__)

from . import views