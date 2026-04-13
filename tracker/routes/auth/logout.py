"""
tracker/routes/auth/logout.py

This file contains the logout route for the MySpend application.
"""

# redirect and url_for are used to redirect users to different pages.
from flask import redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import the shared Blueprint.
from ..main_blueprint import main


# Route to log out the user.
# This clears the session and redirects the user to the login page.
@main.route("/logout")
def logout():
    session.clear()  # Clear all session data (logs the user out).
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("main.login"))