"""
tracker/routes/about.py

This file contains the about page route for the MySpend application.
"""

# render_template is used to render HTML templates.
from flask import render_template

# Import the shared Blueprint.
from .main_blueprint import main


# Route for the about page, which provides information about the MySpend app, its features, and the developer. This page is accessible from the navigation menu and serves to give users a better understanding of what MySpend offers and who created it. The route simply renders the about.html template, which contains the content for the about page.
@main.route("/about")
def about():
    return render_template("about.html")