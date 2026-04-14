"""
tracker/routes/auth/logout.py

This file contains the logout route for the MySpend application.
"""

# redirect and url_for are used to move the user to another route.
from flask import redirect, url_for

# session is used to store and clear user login data.
from flask import session

# flash is used to display messages to the user.
from flask import flash

# Import the shared Blueprint.
from ..main_blueprint import main


# Logout route:
# - clears the user session
# - redirects the user to the login page
@main.route("/logout")
def logout() -> str:
    """
    Handle user logout.

    This route:
    - clears all session data
    - logs the user out
    - redirects to the login page

    Returns:
        str: Redirect response
    """

    # Clear all session data (logs the user out)
    session.clear()

    # Show confirmation message
    flash("You have been logged out successfully.", "success")

    # Redirect to login page
    return redirect(url_for("main.login"))