"""
tracker/routes/__init__.py

This package contains all route modules for the MySpend application.
"""

# Import the shared Blueprint so it can be imported from tracker.routes
from .main_blueprint import main



# Import new modular routes
from . import auth

from . import test_route

from . import home
from . import about
from . import contact
from . import reviews
from . import add_review
from . import overview


from . import dashboard