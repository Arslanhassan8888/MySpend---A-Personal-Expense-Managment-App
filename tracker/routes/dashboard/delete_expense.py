"""
tracker/routes/dashboard/delete_expense.py

This file contains the delete expense route for the MySpend application.
"""

# redirect and url_for are used to redirect users to different pages.
from flask import redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import the get_db_connection function from models.py to interact with the database.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


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
    return redirect(url_for("main.dashboard") + "#expenses")