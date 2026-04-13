"""
tracker/routes/__init__.py

This package contains all route modules for the MySpend application.
"""

# Import the shared Blueprint so it can be imported from tracker.routes
from .main_blueprint import main

# Import old routes (temporary, while refactoring)
from .. import legacy_routes

# Import new modular routes
from . import auth
from . import home
from . import about
from . import contact
from . import reviews
from . import add_review