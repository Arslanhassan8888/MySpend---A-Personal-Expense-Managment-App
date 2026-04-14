"""
tracker/routes/test_route.py

This file contains the test route for the MySpend application.
"""

# Import the shared Blueprint.
from .main_blueprint import main


@main.route("/test")
def test():
    return "This is a test route to check if the Blueprint is working!"