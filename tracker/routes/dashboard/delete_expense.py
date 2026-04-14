"""
tracker/routes/dashboard/delete_expense.py
-----------------------------------------
This file contains the delete expense route for the MySpend application.
"""

# redirect and url_for are used to navigate after actions.
from flask import redirect, url_for

# session is used to check if the user is logged in.
from flask import session

# flash is used to display messages to the user.
from flask import flash

# Import the database connection helper from models.py.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


@main.route("/delete-expense/<int:expense_id>")
def delete_expense(expense_id: int) -> str:
    """
    Delete a specific expense.

    This route:
    - checks that the user is logged in
    - deletes the selected expense (only if it belongs to the user)
    - redirects back to the dashboard

    Args:
        expense_id (int): ID of the expense to delete

    Returns:
        str: Redirect response
    """

    # Ensure the user is logged in before allowing deletion
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the expense only if it belongs to the logged-in user
    cursor.execute(
        "DELETE FROM expenses WHERE expense_id = ? AND user_id = ?",
        (expense_id, session["user_id"])
    )

    # Save changes and close connection
    conn.commit()
    conn.close()

    # Show confirmation message and redirect back to dashboard
    flash("Expense deleted successfully!")
    return redirect(url_for("main.dashboard") + "#expenses")