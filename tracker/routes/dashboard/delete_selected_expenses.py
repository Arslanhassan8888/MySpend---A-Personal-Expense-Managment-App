"""
tracker/routes/dashboard/delete_selected_expenses.py
---------------------------------------------------
This file contains the route for deleting multiple selected expenses.
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


@main.route("/delete-selected-expenses", methods=["POST"])
def delete_selected_expenses() -> str:
    """
    Delete multiple selected expenses.

    This route:
    - checks that the user is logged in
    - retrieves selected expense IDs from the form
    - deletes each expense belonging to the user
    - redirects back to the dashboard with a message

    Returns:
        str: Redirect response
    """

    # Ensure the user is logged in
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Get list of selected expense IDs from the form (checkbox inputs)
    expense_ids = request.form.getlist("expense_ids")

    # If no expenses were selected, show a message
    if not expense_ids:
        flash("No expenses selected")
        return redirect(url_for("main.dashboard") + "#expenses")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete each selected expense, ensuring it belongs to the user
    for expense_id in expense_ids: # We loop through each expense ID in the list of selected expense IDs. For each ID, we execute a SQL query to delete the expense from the database, but only if it belongs to the logged-in user.
        cursor.execute(
            "DELETE FROM expenses WHERE expense_id = ? AND user_id = ?",
            (expense_id, session["user_id"])
        
    )
    # Save changes and close connection
    conn.commit()
    conn.close()

    # Show success message with number of deleted items
    flash(f"{len(expense_ids)} expenses deleted successfully!") # We display a flash message to the user indicating how many expenses were deleted successfully, using the length of the list of selected expense IDs.
    return redirect(url_for("main.dashboard") + "#expenses") # We redirect the user back to the dashboard page, specifically to the expenses section, after the deletion is complete.