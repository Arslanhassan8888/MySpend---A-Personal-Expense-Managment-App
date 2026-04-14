"""
tracker/routes/__init__.py
-------------------------
This package groups all route modules for the MySpend application.

It imports and exposes the main Blueprint, and ensures that all route
files are loaded so their endpoints are registered.
"""

# Import the shared Blueprint so it can be accessed from tracker.routes
from .main_blueprint import main


# Import route modules to register their routes with the Blueprint

# Authentication routes (login, register, logout)
from . import auth

# Test route (used for debugging or development checks)
from . import test_route

# Main site pages
from . import home
from . import about
from . import contact
from . import reviews
from . import add_review
from . import overview

# Dashboard-related routes (expenses, budget, etc.)
from . import dashboard