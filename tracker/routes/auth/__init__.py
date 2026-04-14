"""
tracker/routes/auth/__init__.py

This package groups all authentication-related routes.
"""

# Import authentication modules so Flask registers their routes.
# Each imported file contains route functions linked to the main Blueprint.
from . import logout      # Handles user logout functionality
from . import login       # Handles user login (authentication)
from . import register    # Handles new user registration