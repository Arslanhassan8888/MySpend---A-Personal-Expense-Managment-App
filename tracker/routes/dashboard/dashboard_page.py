"""
tracker/routes/dashboard/dashboard_page.py

This file contains the main dashboard page route for the MySpend application.
"""

# render_template is used to render HTML templates.
# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages after certain actions.
# url_for is used to generate URLs for the specified endpoint (route function).
from flask import render_template, request, redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import datetime and timedelta for handling date and time operations, such as calculating date ranges for expense tracking.
from datetime import datetime, timedelta

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import the get_db_connection function from models.py to interact with the database.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


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