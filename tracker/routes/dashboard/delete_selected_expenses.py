"""
tracker/routes/dashboard/delete_selected_expenses.py

This file contains the delete selected expenses route for the MySpend application.
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

    flash(f"{len(expense_ids)} expenses deleted successfully!")
    return redirect(url_for("main.dashboard") + "#expenses")