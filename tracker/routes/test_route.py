"""
tracker/routes/test_route.py
---------------------------
This file defines a simple test route.

It is used to check that the Blueprint and routing are working correctly.
"""

# Import the shared Blueprint.
from .main_blueprint import main


# STEP 1: Test route
@main.route("/test")
def test() -> str:
    """
    Test that the route system is working.

    This route:
    - returns a simple text response
    - confirms that the Blueprint is registered correctly

    Returns:
        str: Plain text response
    """

    return "This is a test route to check if the Blueprint is working!"*9