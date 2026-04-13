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
    
    if user is None:
        conn.close()
        session.clear()
        flash("Your session has expired. Please log in again.", "error")
        return redirect(url_for("main.login"))

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
    # This route provides an overview of the user's expenses, including daily totals for the past week. It checks if the user is logged in, retrieves the user's name, and then calculates the total expenses for each of the last 7 days. The data is then passed to the overview.html template to be displayed in a chart format.
    # The route first checks if the user is logged in by verifying if "user_id" exists in the session. If not, it redirects the user to the login page. Then it establishes a connection to the database and retrieves the user's name using their user_id from the session. Next, it initializes two lists, daily_labels and daily_values, to store the labels (day names) and corresponding expense totals for each of the last 7 days. It calculates the date for each of the last 7 days, retrieves the total expenses for that day from the database, and appends the results to the respective lists. Finally, it closes the database connection and renders the overview.html template, passing the user's name and the daily labels and values for chart rendering.
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    #open database connection and get user's name to display on the overview page
    conn = get_db_connection()
    cursor = conn.cursor()

    #get the user's name from the database using their user_id stored in the session. This is used to personalize the overview page with a greeting or display the user's name in the header.
    user = cursor.execute(
        "SELECT name FROM users WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()
    
    if user is None:
        conn.close()
        session.clear()
        flash("Your session has expired. Please log in again.", "error")
        return redirect(url_for("main.login"))

    # -----------------------------
    # DAILY CHART DATA
    # -----------------------------
    daily_labels = []
    daily_values = []

    #get the current date and then loop through the last 7 days to calculate the total expenses for each day. For each day, it retrieves the sum of expenses from the database for that specific date and appends the day name (e.g., "Mon", "Tue") to daily_labels and the corresponding total amount to daily_values. This data is then used to render a chart on the overview page that shows the user's spending trends over the past week.
    today = datetime.now().date()

    # Loop through the last 7 days (including today) to get daily totals. The loop starts from 6 and goes down to 0, which allows us to calculate the date for each of the last 7 days by subtracting the appropriate number of days from today's date. For each day, it retrieves the total expenses for that day from the database and appends the results to the daily_labels and daily_values lists.
    for i in range(6, -1, -1):
        # Calculate the date for the current day in the loop by subtracting i days from today's date. This allows us to get the date for each of the last 7 days, starting from 6 days ago up to today. The day_name variable is then set to the abbreviated name of the day (e.g., "Mon", "Tue") using strftime, which is used as a label for the chart.
        day = today - timedelta(days=i)
        #thse labels will be used on the x-axis of the daily expenses chart to indicate which day each data point corresponds to. For example, if today is Wednesday, the labels for the last 7 days would be ["Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed"].
        day_name = day.strftime("%a")

        # Retrieve the total expenses for the current day from the database
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ? AND date = ?
            """,
            (session["user_id"], day.isoformat())
        ).fetchone()[0]

        # If there are no expenses for that day, the result will be None. In that case, we set it to 0 to ensure that the chart displays a value of 0 instead of being empty or showing an error.
        if result is None:
            result = 0

        # Append the day name and total expenses to the respective lists. The day_name is added to daily_labels, which will be used as labels on the x-axis of the chart, while the total expenses (converted to a float) are added to daily_values, which will be used as data points on the y-axis of the chart.
        daily_labels.append(day_name)
        # Convert the result to a float and append it to daily_values. This ensures that the values are in a consistent format for chart rendering, even if the database returns them as integers or None (which we already handled by setting it to 0).
        daily_values.append(float(result))
        
    
    # WEEKLY CHART DATA
    # -----------------------------
       # -----------------------------
    # WEEKLY CHART DATA
    # -----------------------------
    # This section prepares the weekly spending chart data using the same simple
    # Method A structure as the daily chart. We create two separate lists:
    # weekly_labels and weekly_values. The labels will be used on the x-axis of
    # the chart, while the values will be used for the height of the bars.
    # This keeps the code beginner friendly and makes the flow easy to understand:
    # Python prepares the data, the template stores it in HTML data attributes,
    # and JavaScript reads those values to build the chart.
    
    # Create two temporary lists to hold the weekly chart labels and values.
    # The labels will be simple names such as Week 1, Week 2, Week 3, and Week 4.
    # The values will store the total amount spent during each of those weeks.
    weekly_labels = []
    weekly_values = []

    # Get today's date again so we can work backwards through the last 4 weeks.
    # Each week in this chart is a 7 day block, and we will compare the total
    # spending for each of those blocks.
    today = datetime.now().date()

    # Loop through the last 4 weeks, starting from the oldest week and ending
    # with the most recent week. This allows the chart to display in a natural
    # left-to-right order for easier reading.
    for i in range(3, -1, -1):

        # Calculate how many days back the current week starts and ends.
        # Example:
        # i = 3 means the oldest week in the last 4 weeks
        # i = 0 means the most recent week
        days_back_start = (i * 7) + 6
        days_back_end = i * 7

        # Calculate the date range for this 7 day period.
        week_start = today - timedelta(days=days_back_start)
        week_end = today - timedelta(days=days_back_end)

        # Create a simple label for the chart.
        # This keeps the output beginner friendly and easy for the user to read.
        week_number = 4 - i
        week_label = f"Week {week_number}"

        # Query the database to find the total spending during this week range.
        # The BETWEEN clause includes both the start date and end date.
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            AND date BETWEEN ? AND ?
            """,
            (session["user_id"], week_start.isoformat(), week_end.isoformat())
        ).fetchone()[0]

        # If there are no expenses in that week, SQLite returns None.
        # Change it to 0 so the chart can still display correctly.
        if result is None:
            result = 0

        # Add the label and value to the temporary weekly lists.
        weekly_labels.append(week_label)
        weekly_values.append(float(result))

        # -----------------------------
    # MONTHLY CHART DATA
    # -----------------------------
    # This section prepares the monthly spending chart data using the same simple
    # Method A structure as the daily and weekly charts. We create two separate
    # lists called monthly_labels and monthly_values. The labels will be the month
    # names from January to December, and the values will be the total spending
    # for each month in the current year. This keeps the flow clear and easy to
    # follow: Python prepares the data, the template stores it in HTML data
    # attributes, and JavaScript reads the values to build the chart.

    # Create two empty lists to hold the month names and the matching totals.
    monthly_labels = []
    monthly_values = []

    # Get the current year so the chart only shows data for this year.
    # For example, if the current year is 2026, the chart will compare
    # spending from January 2026 to December 2026.
    current_year = datetime.now().year

    # Loop through all 12 months of the year.
    # The loop starts at 1 for January and ends at 12 for December.
    for month_number in range(1, 13):

        # Create a date object for the first day of the current month in the loop.
        # This is used to create a short month label such as Jan, Feb, Mar, and so on.
        month_date = datetime(current_year, month_number, 1)
        month_label = month_date.strftime("%b")

        # Create a year-month string in the format YYYY-MM.
        # This matches the format used by SQLite with strftime('%Y-%m', date).
        # Example: "2026-01" for January 2026.
        year_month = month_date.strftime("%Y-%m")

        # Query the database to find the total amount spent during this month.
        # The query adds together all expense amounts for the logged-in user
        # where the expense date falls inside the current month of the current year.
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            AND strftime('%Y-%m', date) = ?
            """,
            (session["user_id"], year_month)
        ).fetchone()[0]

        # If there are no expenses for that month, SQLite returns None.
        # Change it to 0 so the chart can still display an empty month correctly.
        if result is None:
            result = 0

        # Add the short month label and the total amount to the two lists.
        # The month label will be used on the x-axis, and the total value
        # will be used on the y-axis of the monthly chart.
        monthly_labels.append(month_label)
        monthly_values.append(float(result))
    
        # -----------------------------
    # CATEGORY PIE CHART DATA
    # -----------------------------
    # This section prepares the category pie chart data using the same simple
    # Method A structure as the other charts. We create two separate lists:
    # category_labels and category_values. The labels will contain the category
    # names, and the values will contain the total amount spent in each category
    # for the current month. This allows the pie chart to show how the user's
    # spending is divided across categories during the current month.

    # Create two empty lists to hold the category names and the matching totals.
    category_labels = []
    category_values = []

    # Create a year-month value for the current month.
    # This allows us to only include expenses from the current month
    # when building the category breakdown.
    current_year_month = datetime.now().strftime("%Y-%m")

       # Query the database to get all categories, even if some categories have
    # no expenses in the current month. We use a LEFT JOIN so every category
    # from the categories table is still returned. If a category has no matching
    # expense in the current month, its total will become 0.
    category_rows = cursor.execute(
        """
        SELECT categories.name, COALESCE(SUM(expenses.amount), 0) AS total_amount
        FROM categories
        LEFT JOIN expenses
            ON expenses.category_id = categories.category_id
            AND expenses.user_id = ?
            AND strftime('%Y-%m', expenses.date) = ?
        GROUP BY categories.category_id, categories.name
        ORDER BY categories.name ASC
        """,
        (session["user_id"], current_year_month)
    ).fetchall()

    # Loop through the query results and place each category name and total
    # into the matching lists. These lists will later be passed into the
    # overview template and used by JavaScript to build the pie chart.
    for row in category_rows:
        category_labels.append(row["name"])
        category_values.append(float(row["total_amount"]))

    conn.close()
    # Send the chart data to the overview.html template.
    # The template will use daily_labels and daily_values for the daily line chart,
    # weekly_labels and weekly_values for the weekly bar chart,
    # monthly_labels and monthly_values for the monthly line chart,
    # and category_labels and category_values for the category pie chart.
    # The user's name is also passed so the page can remain personalised.
    return render_template(
        "overview.html",
        name=user["name"],
        daily_labels=daily_labels,
        daily_values=daily_values,
        weekly_labels=weekly_labels,
        weekly_values=weekly_values,
        monthly_labels=monthly_labels,
        monthly_values=monthly_values,
        category_labels=category_labels,
        category_values=category_values
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

# Route for the about page, which provides information about the MySpend app, its features, and the developer. This page is accessible from the navigation menu and serves to give users a better understanding of what MySpend offers and who created it. The route simply renders the about.html template, which contains the content for the about page.
@main.route("/about")
def about():
    return render_template("about.html")

# Route for the reviews page, which displays user reviews and testimonials
# about the MySpend app. This page is accessible from the navigation menu
# and retrieves all reviews from the database, showing the newest first.
@main.route("/reviews")
def reviews():

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all reviews from newest inserted to oldest inserted
    reviews = cursor.execute("""
        SELECT reviewer_name, location, rating, review_text
        FROM reviews
        ORDER BY review_id DESC
    """).fetchall()

    # Close the connection
    conn.close()

    # Show the Reviews page
    return render_template("reviews.html", reviews=reviews)

# The add_review route allows logged-in users to submit their reviews about the MySpend app. When a user tries to access this page, the route first checks if they are logged in by verifying if "user_id" exists in the session. If the user is not logged in, they are redirected to the login page with a flash message prompting them to log in to leave a review. If the user is logged in, the route then connects to the database and checks if the user has already submitted a review by querying the reviews table for any existing review associated with their user_id. If an existing review is found, the user is redirected back to the reviews page with a flash message indicating that they have already submitted a review. If no existing review is found, the route renders the add_review.html template, allowing the user to fill out and submit their review for MySpend.
# This functionality ensures that each user can only submit one review, preventing duplicate reviews and encouraging users to provide thoughtful feedback about their experience with the app. It also maintains the integrity of the reviews section by ensuring that the feedback is genuine and not spammed with multiple entries from the same user.
@main.route("/add-review", methods=["GET"])
def add_review():

    # Only logged-in users can access this page
    if "user_id" not in session:
        flash("Please log in to leave a review.", "error")
        return redirect(url_for("main.login"))

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check whether this user has already submitted a review
    existing_review = cursor.execute(
        "SELECT review_id FROM reviews WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    # If the user already has a review, send them back
    if existing_review:
        flash("You have already submitted a review.", "error")
        return redirect(url_for("main.reviews"))

    # Show the add review page
    return render_template("add_review.html")