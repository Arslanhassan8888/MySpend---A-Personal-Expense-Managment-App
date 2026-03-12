"""
tracker/routes.py
This file defines the URL routes for the MySpend application.

Routes determine:
- What happens when a user visits a specific URL.
- Which function should execute.
- What response should be returned.

Blueprints are used to:
- Organize routes into modular components.
- Keep the project scalable and clean.
"""

# Import Blueprint from Flask.
# A Blueprint is used to group related routes.
# render_template is used to render HTML templates.
# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages after certain actions (like registration).
# url_for is used to generate URLs for the specified endpoint (route function).
from flask import Blueprint, render_template, request, redirect, url_for
# Import the get_db_connection function from models.py to interact with the database.
from .models import get_db_connection
# Import generate_password_hash to securely hash user passwords before storing them in the database.
# werkzeug.security is a module that provides utilities for hashing passwords and checking hashed passwords.
from werkzeug.security import check_password_hash, generate_password_hash
# Import session to manage user sessions (e.g., keeping users logged in).
from  flask import session

# "main" is the name of this Blueprint.
# __name__ helps Flask locate resources correctly.
main = Blueprint("main", __name__)

@main.route("/test")
def test():
    return "This is a test route to check if the Blueprint is working!"

# This route handles requests to the root URL "/".
# When a user visits:
# http://127.0.0.1:5000/
# this function will execute.
@main.route("/")
def home():
    
    user_id = session.get("user_id")  # Get the user_id from the session, if it exists.
    
    # Render the index.html template when the root URL is accessed.
    return render_template("index.html", user_id=user_id)  # Pass user_id to the template for conditional display.

# Register route
# This route handles BOTH:
# - displaying the registration page
# - processing the registration form
@main.route("/register", methods=["GET", "POST"])
def register():
    
    error = None  # Initialize error variable to None
    # If the user submitted the form
    if request.method == "POST":

        # Get form data from the registration form
        email = request.form["email"].strip().lower()  # Remove leading/trailing whitespace and convert to lowercase
        password = request.form["password"]

        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()

       # Check if the email already exists "? mean parameterized query to prevent SQL injection" means that the value of email will be safely inserted into the SQL query,
       # preventing malicious input from breaking the query or accessing unauthorized data. The actual value of email is passed as a tuple (email,) to the execute method, 
       # which ensures that it is treated as a parameter rather than part of the SQL command.
        existing_user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,) # Note the comma to make it a tuple
        ).fetchone() # fetchone() retrieves the first row of the result, or None if there are no results.

        # If email exists, show error message
        if existing_user:
            conn.close()  # Close the database connection
            error = "Email already registered"
            return render_template("register.html", error=error)   # Render the registration page with the error message    

        else:
            # Hash the password
            password_hash = generate_password_hash(password)

            # Insert new user into database
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash)
            )

        # Save changes
        conn.commit()

        # Close connection
        conn.close()

        # Redirect user to login page
        return redirect(url_for("main.login")) # url_for("main.home") generates the URL for the home route defined in this Blueprint.

    # If user simply opened /register page
    return render_template("register.html", error=error)

# Login route handles both:
# - displaying the login page
@main.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"].strip().lower()  # Remove leading/trailing whitespace from email input
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        # Check if user exists and password matches
        if user and check_password_hash(user["password_hash"], password):

            # Store user id in session
            # session is a special object in Flask that allows you to store information across requests.
            session["user_id"] = user["user_id"]
            
            

            return redirect(url_for("main.home"))

        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)