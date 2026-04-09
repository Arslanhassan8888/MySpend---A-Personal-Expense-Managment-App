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
                session["name"] = user["name"]

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

        flash("Expense added successfully!")  # Flash a success message to the user
        return redirect(url_for("main.dashboard")+ "#expenses")  # Redirect to the dashboard and scroll to the expenses section


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

    # Remove the user_id from the session
    session.pop("user_id", None)

    # Redirect user to the home page
    return redirect(url_for("main.home"))

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