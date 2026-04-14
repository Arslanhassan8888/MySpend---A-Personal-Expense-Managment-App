"""
tracker/routes/dashboard/update_expense.py

This file contains the update expense route for the MySpend application.
"""

# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages.
from flask import request, redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users.
from flask import flash

# Import the get_db_connection function from models.py to interact with the database.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


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