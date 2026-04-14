"""
tracker/routes/dashboard/update_expense.py
-----------------------------------------
This file contains the update expense route for the MySpend application.
"""

# request is used to access form data sent by the user.
# redirect and url_for are used to navigate after actions.
from flask import request, redirect, url_for

# session is used to check if the user is logged in.
from flask import session

# flash is used to display messages to the user.
from flask import flash

# Import the database connection helper from models.py.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


@main.route("/update-expense", methods=["POST"])
def update_expense() -> str:
    """
    Update an existing expense.

    This route:
    - checks that the user is logged in
    - retrieves updated form values
    - updates the selected expense in the database
    - ensures the expense belongs to the user
    - redirects back to the dashboard

    Returns:
        str: Redirect response
    """

    # Ensure the user is logged in
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Get updated values from the form
    expense_id = request.form["expense_id"]
    amount = request.form["amount"]
    category_id = request.form["category_id"]
    date = request.form["date"]
    description = request.form["description"].strip()

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the expense only if it belongs to the logged-in user
    cursor.execute(
        """
        UPDATE expenses
        SET amount = ?, category_id = ?, date = ?, description = ?
        WHERE expense_id = ? AND user_id = ?
        """,
        (amount, category_id, date, description, expense_id, session["user_id"])
    )

    # Save changes and close connection
    conn.commit()
    conn.close()

    # Show confirmation message and redirect back to dashboard
    flash("Expense updated successfully!")
    return redirect(url_for("main.dashboard") + "#expenses")