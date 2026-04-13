"""
tracker/routes/main_blueprint.py

This file creates the shared Blueprint used by all route modules.
"""

# Import Blueprint from Flask.
# A Blueprint is used to group related routes.
from flask import Blueprint

# "main" is the name of this Blueprint.
# __name__ helps Flask locate resources correctly.
main = Blueprint("main", __name__)