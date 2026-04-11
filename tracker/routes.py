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
from flask import flash  # Import flash for displaying messages to users (e.g., success or error messages)

# jason used to convert API resonse to a Python dictionary
import json
# used to call external APIs, Requests is a popular library for making HTTP requests in Python. It simplifies the process of sending HTTP requests and handling responses.
from urllib.request import urlopen, Request
# used to handle URL errors when calling external APIs, such as network issues or invalid URLs. URLError is raised when there is a problem with the network connection or the URL is invalid, 
# while HTTPError is raised when the server returns an HTTP error status code (e.g., 404 Not Found, 500 Internal Server Error).
from urllib.error import URLError, HTTPError
#we use it for fallback qoutes if API is not working, it allows us to select a random quote from a predefined list of quotes.
import random

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
    
    # Get a random motivational quote (API or fallback)
    quote = get_home_quote()
    
    # Render the index.html template when the root URL is accessed.
    # Pass the quote and user_id to the template for dynamic content rendering.
    # send quote text, author, and source to the template to display on the homepage. Also send user_id to conditionally show different content for logged-in users vs guests.
    return render_template(
        "index.html",
        user_id=user_id,  # Pass user_id to the template for conditional display.
        quote_text=quote["text"],
        quote_author=quote["author"],
        quote_source=quote["source"]
    )
    
@main.route("/register", methods=["GET", "POST"])
def register():

    error = None
    entered_name = ""
    entered_email = ""

    if request.method == "POST":

        entered_name = request.form.get("name", "").strip()
        entered_email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        agree_terms = request.form.get("agree_terms")

        # REQUIRED FIELDS
        if entered_name == "" or entered_email == "" or password == "" or confirm_password == "":
            error = "Please fill in all fields."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # TERMS CHECKBOX
        if not agree_terms:
            error = "You must agree to the Terms of Service and Privacy Policy."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # SIMPLE EMAIL VALIDATION
        if "@" not in entered_email or "." not in entered_email:
            error = "Please enter a valid email address."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        # CHECK IF EMAIL ALREADY EXISTS
        existing_user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (entered_email,)
        ).fetchone()

        if existing_user:
            conn.close()
            error = "Email already registered."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # PASSWORD MATCH
        if password != confirm_password:
            conn.close()
            error = "Passwords do not match."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # PASSWORD RULES
        has_number = any(char.isdigit() for char in password)
        has_special = any(not char.isalnum() for char in password)

        if len(password) < 12:
            conn.close()
            error = "Password must be at least 12 characters long."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        if not has_number:
            conn.close()
            error = "Password must contain at least one number."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        if not has_special:
            conn.close()
            error = "Password must contain at least one special character."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (entered_name, entered_email, password_hash)
        )

        conn.commit()
        conn.close()

        success = "Registration completed successfully. Redirecting to login page..."

        return render_template(
            "register.html",
            success=success,
            entered_name="",
            entered_email=""
        )

    return render_template(
        "register.html",
        error=error,
        entered_name=entered_name,
        entered_email=entered_email
    )

# Login route handles both:
# - displaying the login page
@main.route("/login", methods=["GET", "POST"])
def login():

    error = None
    entered_email = ""

    if request.method == "POST":

        entered_email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # REQUIRED FIELDS
        if entered_email == "" or password == "":
            error = "Please fill in all fields."
            return render_template(
                "login.html",
                error=error,
                entered_email=entered_email
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (entered_email,)
        ).fetchone()

        # EMAIL NOT REGISTERED
        if not user:
            conn.close()
            error = "Invalid email or password."
            return render_template(
                "login.html",
                error=error,
                entered_email=entered_email
            )

        # CHECK LOCK FOR THIS ACCOUNT ONLY
        if user["lockout_until"] is not None:
            lock_time = datetime.fromisoformat(user["lockout_until"])

            if datetime.now() < lock_time:
                conn.close()
                error =  "Too many failed login attempts. Please try again in 5 minutes."
                return render_template(
                    "login.html",
                    error=error,
                    entered_email=entered_email
                )

        # CORRECT PASSWORD
        if check_password_hash(user["password_hash"], password):

            cursor.execute(
                "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE user_id = ?",
                (user["user_id"],)
            )

            conn.commit()
            conn.close()

            session.clear()
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]

            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))

        # WRONG PASSWORD FOR A REGISTERED EMAIL
        attempts = user["failed_attempts"] + 1

        if attempts >= 3:
            lock_time = datetime.now() + timedelta(minutes=5)

            cursor.execute(
                "UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE user_id = ?",
                (attempts, lock_time.isoformat(), user["user_id"])
            )

            error = "Too many failed login attempts. Please try again in 5 minutes."

        else:
            cursor.execute(
                "UPDATE users SET failed_attempts = ? WHERE user_id = ?",
                (attempts, user["user_id"])
            )

            remaining = 3 - attempts
            error = f"Incorrect password. You have {remaining} attempt(s) remaining."

        conn.commit()
        conn.close()

    return render_template(
        "login.html",
        error=error,
        entered_email=entered_email
    )
# Dashboard route - shows user-specific information after login
@main.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    # USER
    user = cursor.execute(
        "SELECT name FROM users WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    # SORT
    sort = request.args.get("sort")

    if not sort:
        sort = "date_desc"

    order_clause = {
        "date_desc": "expenses.date DESC",
        "date_asc": "expenses.date ASC",
        "amount_asc": "expenses.amount ASC",
        "amount_desc": "expenses.amount DESC",
        "category_asc": "categories.name ASC",
        "category_desc": "categories.name DESC",
        "desc_asc": "expenses.description ASC",
        "desc_desc": "expenses.description DESC"
    }.get(sort, "expenses.date DESC")

    # SEARCH FILTERS
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    min_amount = request.args.get("min_amount")
    max_amount = request.args.get("max_amount")
    description = request.args.get("description")
    category_id = request.args.get("category_id")

    # BASE QUERY
    query = f"""
    SELECT expenses.expense_id, expenses.date, expenses.amount, expenses.description, categories.name, expenses.category_id
    FROM expenses
    JOIN categories ON expenses.category_id = categories.category_id
    WHERE expenses.user_id = ?
    """

    params = [session["user_id"]]

    # APPLY FILTERS (only if user entered values)

    if date_from and date_from != "":
        query += " AND expenses.date >= ?"
        params.append(date_from)

    if date_to and date_to != "":
        query += " AND expenses.date <= ?"
        params.append(date_to)

    if min_amount and min_amount != "":
        query += " AND expenses.amount >= ?"
        params.append(min_amount)

    if max_amount and max_amount != "":
        query += " AND expenses.amount <= ?"
        params.append(max_amount)

    if description and description != "":
        query += " AND expenses.description LIKE ?"
        params.append(f"%{description}%")
        
    if category_id and category_id != "":
        query += " AND expenses.category_id = ?"
        params.append(category_id)

    # SORT
    query += f" ORDER BY {order_clause}"

    # EXECUTE
    expenses = cursor.execute(query, params).fetchall()

    # TOTAL
    total = cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]

    # MONTHLY TOTAL
    monthly_total = cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """,
        (session["user_id"],)
    ).fetchone()[0]
    
    month = datetime.now().strftime("%Y-%m")

    budget = cursor.execute("""
        SELECT amount FROM budgets
        WHERE user_id = ? AND month = ?
    """, (session["user_id"], month)).fetchone()

    budget_amount = budget[0] if budget else 0

    remaining = budget_amount - monthly_total
    # Calculate progress percentage for the budget. If the budget amount is greater than 0, calculate the percentage of the budget that has been used based on the monthly total. If the budget amount is 0 or less, set progress to 0 to avoid division by zero.
    if budget_amount > 0:
        progress = (monthly_total/ budget_amount) * 100
    else:
        progress = 0
        
    # DAILY TOTAL
    daily_total = cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND date = DATE('now')
        """,
        (session["user_id"],)
    ).fetchone()[0]

    weekly_total = cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
         AND date BETWEEN DATE('now', 'weekday 1', '-7 days')
                  AND DATE('now', 'weekday 0')
        """,
        (session["user_id"],)
    ).fetchone()[0]
    categories = cursor.execute(
    "SELECT * FROM categories"
).fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        name=user["name"],
        expenses=expenses,
        total=total,
        monthly_total=monthly_total,
        daily_total=daily_total,
        weekly_total=weekly_total,
        categories=categories,
        budget_amount=budget_amount,
        remaining=remaining,
        progress=progress,
        current_month=datetime.now().strftime("%B %Y")
        
    )

@main.route("/add-expense", methods=["POST"])
def add_expense():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                flash("Amount must be greater than zero.")
                return redirect(url_for("main.dashboard") + "#expenses")
        except ValueError:
            flash("Invalid amount. Please enter a valid number.")
            return redirect(url_for("main.dashboard") + "#expenses")

        category_id = request.form["category_id"]
        date = request.form["date"]
        description = request.form["description"].strip()

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

        flash("Expense added successfully!", "success")  # Flash a success message to the user
        return redirect(url_for("main.dashboard")+ "#add-expense")  # Redirect to the dashboard and scroll to the expenses section


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

    flash("Expense deleted successfully!")  # Flash a success message to the user
    return redirect(url_for("main.dashboard") + "#expenses")  # Redirect to the dashboard and scroll to the expenses section    

@main.route("/delete-selected-expenses", methods=["POST"])
def delete_selected_expenses():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    expense_ids = request.form.getlist("expense_ids")

    if not expense_ids:
        flash("No expenses selected")
        return redirect(url_for("main.dashboard") + "#expenses")

    conn = get_db_connection()
    cursor = conn.cursor()

    for expense_id in expense_ids:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_id = ? AND user_id = ?",
            (expense_id, session["user_id"])
        )

    conn.commit()
    conn.close()

    flash(f"{len(expense_ids)} expenses deleted successfully!")  # Flash a success message indicating how many expenses were deleted
    return redirect(url_for("main.dashboard") + "#expenses")  # Redirect to the dashboard and scroll to the expenses section

@main.route("/logout")
def logout():

    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("main.login"))

@main.route("/update-expense", methods=["POST"])
def update_expense():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    expense_id = request.form["expense_id"]
    amount = request.form["amount"]
    category_id = request.form["category_id"]
    date = request.form["date"]
    description = request.form["description"].strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET amount = ?, category_id = ?, date = ?, description = ?
        WHERE expense_id = ? AND user_id = ?
        """,
        (amount, category_id, date, description, expense_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    flash("Expense updated successfully!")  # Flash a success message to the user
    return redirect(url_for("main.dashboard") + "#expenses")

@main.route("/set-budget", methods=["POST"])
def set_budget():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    raw_amount = request.form.get("budget_amount", "").strip()

    # EMPTY INPUT
    if raw_amount == "":
        flash("Please enter a budget amount.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    # NOT A NUMBER
    try:
        amount = float(raw_amount)
    except ValueError:
        flash("Please enter a valid number.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    # NEGATIVE OR ZERO
    if amount <= 0:
        flash("Budget must be greater than zero.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    month = datetime.now().strftime("%Y-%m")

    conn = get_db_connection()
    cursor = conn.cursor()

    existing = cursor.execute("""
        SELECT * FROM budgets
        WHERE user_id = ? AND month = ?
    """, (session["user_id"], month)).fetchone()

    if existing:
        cursor.execute("""
            UPDATE budgets
            SET amount = ?
            WHERE user_id = ? AND month = ?
        """, (amount, session["user_id"], month))
    else:
        cursor.execute("""
            INSERT INTO budgets (user_id, amount, month)
            VALUES (?, ?, ?)
        """, (session["user_id"], amount, month))

    conn.commit()
    conn.close()

    flash("Budget set successfully!", "success")
    return redirect(url_for("main.dashboard") + "#budget")

@main.route("/overview")
def overview():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT name FROM users WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template(
        "overview.html",
        name=user["name"]
    )
    
# This function calls an external API to get a random quote for the homepage. If the API call fails for any reason (network issues, API downtime, etc.), 
# it falls back to a predefined list of quotes to ensure that the homepage always has a quote to display. 
# The function returns a dictionary containing the quote text, author, and source (either "ZenQuotes" for API or "MySpend" for fallback).
#zenquotes.io is a free API that provides random inspirational quotes. But since it's a free service, it can sometimes be unreliable or slow. Also has no key and limited requests per hour. So we need a fallback mechanism to ensure that our app can still provide value to users even when the API is not working.

def get_home_quote():
    url = "https://zenquotes.io/api/random"

    fallback_quotes = [
        ("A budget is telling your money where to go instead of wondering where it went.", "Dave Ramsey"),
        ("Do not save what is left after spending, but spend what is left after saving.", "Warren Buffett"),
        ("Small daily money habits create long-term financial success.", "Arslan Hassan"),
        
    ]

    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urlopen(request, timeout=5)

        data = json.loads(response.read().decode("utf-8"))

        if isinstance(data, list) and len(data) > 0:
            quote = data[0]

            return {
                "text": quote.get("q", "Stay consistent with your money habits!"),
                "author": quote.get("a", "Arslan Hassan"),
                "source": "ZenQuotes"
            }

    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError):
        pass

    # fallback if API fails
    text, author = random.choice(fallback_quotes)

    return {
        "text": text,
        "author": author,
        "source": "MySpend"
    }