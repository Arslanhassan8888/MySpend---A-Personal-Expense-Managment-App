"""
tracker/routes/dashboard/set_budget.py
-------------------------------------
This file contains the set budget route for the MySpend application.
"""

# request is used to access form data sent by the user.
# redirect and url_for are used to navigate after actions.
from flask import request, redirect, url_for

# session is used to check if the user is logged in.
from flask import session

# flash is used to display messages to the user.
from flask import flash

# datetime is used to determine the current month.
from datetime import datetime

# Import the database connection helper from models.py.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


@main.route("/set-budget", methods=["POST"])
def set_budget() -> str:
    """
    Set or update the user's monthly budget.

    This route:
    - checks that the user is logged in
    - validates the budget input
    - updates the budget if it already exists
    - inserts a new budget if not
    - redirects back to the dashboard

    Returns:
        str: Redirect response
    """

    # Ensure the user is logged in
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Get the entered budget amount and remove extra spaces
    raw_amount = request.form.get("budget_amount", "").strip() # We retrieve the budget amount from the form data using request.form.get("budget_amount"). We also use .strip() to remove any leading or trailing whitespace from the input0.
    if raw_amount == "": # We check if the raw_amount is an empty string, which would indicate that the user did not enter any value for the budget. 
        flash("Please enter a budget amount.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    # NOT A NUMBER
    # Convert input to float and handle invalid values
    try: # We attempt to convert the raw_amount string to a float. If the input is not a valid number (e.g., it contains letters or special characters), a ValueError will be raised, which we catch in the except block to show an error message to the user.
        amount = float(raw_amount)  # We convert the cleaned raw_amount string to a float.
    except ValueError:
        flash("Please enter a valid number.", "error")
        return redirect(url_for("main.dashboard") + "#budget")  

    # NEGATIVE OR ZERO
    # Ensure the budget is a positive value
    if amount <= 0: # We check if the amount is less than or equal to zero, which would indicate an invalid budget value.
        flash("Budget must be greater than zero.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    # Get current month in YYYY-MM format
    month = datetime.now().strftime("%Y-%m") # We determine the current month using datetime.now() and format it as a string in the "YYYY-MM" format (e.g., "2024-01") using strftime.

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if a budget already exists for this user and month
    # We execute a SQL query to check if there is already a budget record in the database for the logged-in user and the current month. If a record exists, it will be returned; otherwise, None will be returned.
    existing = cursor.execute("""
        SELECT * FROM budgets
        WHERE user_id = ? AND month = ?
    """, (session["user_id"], month)).fetchone()

    # If budget exists, update it
    if existing:
        cursor.execute("""
            UPDATE budgets
            SET amount = ?
            WHERE user_id = ? AND month = ?
        """, (amount, session["user_id"], month))
    else:
        # Otherwise, insert a new budget record
        cursor.execute("""
            INSERT INTO budgets (user_id, amount, month)
            VALUES (?, ?, ?)
        """, (session["user_id"], amount, month))

    # Save changes and close connection
    conn.commit()
    conn.close()

    # Show confirmation and redirect back to dashboard
    flash("Budget set successfully!", "success")
    return redirect(url_for("main.dashboard") + "#budget")