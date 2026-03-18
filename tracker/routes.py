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
# Import datetime and timedelta for handling date and time operations, such as calculating date ranges for expense tracking.
from datetime import datetime, timedelta

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
        name = request.form["name"].strip()  # Remove leading/trailing whitespace from name input
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
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash)
            )

        # Save changes
        conn.commit()

        # Close connection
        conn.close()

       # After successful registration, redirect to a success page or login page
        return render_template("register_success.html")

    # If user simply opened /register page
    return render_template("register.html", error=error)

# Login route handles both:
# - displaying the login page
@main.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user:

            # Check if account is locked
            if user["lockout_until"] is not None:
                lock_time = datetime.fromisoformat(user["lockout_until"])

                if datetime.now() < lock_time:
                    error = "Account locked. Try again later."
                    conn.close()
                    return render_template("login.html", error=error)

            # Check password
            if check_password_hash(user["password_hash"], password):

                # Reset failed attempts
                cursor.execute(
                    "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE user_id = ?",
                    (user["user_id"],)
                )

                conn.commit()
                conn.close()

                session["user_id"] = user["user_id"]

                return redirect(url_for("main.dashboard"))

            else:

                attempts = user["failed_attempts"] + 1

                if attempts >= 3:

                    lock_time = datetime.now() + timedelta(minutes=15)

                    cursor.execute(
                        "UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE user_id = ?",
                        (attempts, lock_time.isoformat(), user["user_id"])
                    )

                    error = "Too many failed attempts. Account locked for 15 minutes."

                else:

                    cursor.execute(
                        "UPDATE users SET failed_attempts = ? WHERE user_id = ?",
                        (attempts, user["user_id"])
                    )

                    remaining = 3 - attempts
                    error = f"Invalid login. {remaining} attempts remaining."

                conn.commit()

        else:
            error = "Invalid email or password"

        conn.close()

    return render_template("login.html", error=error)

# Dashboard route - shows user-specific information after login
@main.route("/dashboard")
def dashboard():
    # Check if user is logged in by verifying if "user_id" exists in the session.
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    # Fetch the user's name using their user_id stored in the session. This is used to personalize the dashboard.
    user = cursor.execute(
        "SELECT name FROM users WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()
    # Fetch the user's expenses along with category names using a JOIN query.
    # This query retrieves the expense_id, date, amount, description from the expenses table and the corresponding category name from the categories table.
    # The results are ordered by date in descending order, showing the most recent expenses first.
    expenses = cursor.execute(
        """
        SELECT expenses.expense_id, expenses.date, expenses.amount, expenses.description, categories.name
        FROM expenses
        JOIN categories ON expenses.category_id = categories.category_id
        WHERE expenses.user_id = ?
        ORDER BY expenses.date DESC 
        """,
        (session["user_id"],)
    ).fetchall()
    
    # Calculate total spending for the user by summing the amount column from the expenses table for the logged-in user.
    total = cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]
    
    # TOTAL FOR CURRENT MONTH
    monthly_total = cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """,
        (session["user_id"],)
    ).fetchone()[0]
    
    # TOTAL FOR CURRENT WEEK
    daily_total = cursor.execute(
    """
    SELECT COALESCE(SUM(amount), 0)
    FROM expenses
    WHERE user_id = ?
    AND date = DATE('now')
    """,
    (session["user_id"],)
).fetchone()[0]
    

    # If user has no expenses yet
    if total is None:
        total = 0
    
    conn.close()

    return render_template("dashboard.html", name=user["name"], expenses=expenses, total=total,monthly_total=monthly_total, daily_total=daily_total)

@main.route("/add-expense", methods=["POST"])
def add_expense():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":

        amount = request.form["amount"]
        category_id = request.form["category_id"]
        date = request.form["date"]
        description = request.form["description"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (user_id, category_id, date, amount, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session["user_id"], category_id, date, 
             amount, description)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("main.dashboard"))


@main.route("/delete-expense/<int:expense_id>")
def delete_expense(expense_id):

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE expense_id = ? AND user_id = ?",
        (expense_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect(url_for("main.dashboard"))

@main.route("/delete-selected-expenses", methods=["POST"])
def delete_selected_expenses():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    expense_ids = request.form.getlist("expense_ids")

    conn = get_db_connection()
    cursor = conn.cursor()

    for expense_id in expense_ids:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_id = ? AND user_id = ?",
            (expense_id, session["user_id"])
        )

    conn.commit()
    conn.close()

    return redirect(url_for("main.dashboard"))

@main.route("/logout")
def logout():

    # Remove the user_id from the session
    session.pop("user_id", None)

    # Redirect user to the home page
    return redirect(url_for("main.home"))

