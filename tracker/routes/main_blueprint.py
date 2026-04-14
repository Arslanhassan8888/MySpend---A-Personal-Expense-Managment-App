"""
tracker/routes/main_blueprint.py
-------------------------------
This file creates the shared Blueprint used across all route modules.

The Blueprint allows routes to be organised and registered in one place.
"""

# Blueprint is used to group related routes into a single component.
from flask import Blueprint


# Create shared Blueprint
# "main" is the name of the Blueprint used throughout the application.
# __name__ helps Flask locate templates and static files correctly.
main = Blueprint("main", __name__)