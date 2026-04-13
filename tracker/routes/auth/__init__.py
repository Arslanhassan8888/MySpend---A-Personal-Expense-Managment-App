"""
tracker/routes/auth/__init__.py

This package contains authentication route modules.
"""

# Import authentication route modules so Flask can register them.
from . import logout
from . import login
from . import register