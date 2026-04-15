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
    - validates the submitted values
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
    expense_id = request.form.get("expense_id", "").strip()
    raw_amount = request.form.get("amount", "").strip()
    category_id = request.form.get("category_id", "").strip()
    date = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip()

    # VALIDATE AMOUNT FIELD
    # Ensure the amount field is not empty before trying to convert it.
    if raw_amount == "":
        return redirect(
            url_for(
                "main.dashboard",
                open_modal="edit",
                edit_error="Please enter an amount.",
                edit_expense_id=expense_id,
                edit_amount_value=raw_amount,
                edit_category_value=category_id,
                edit_date_value=date,
                edit_description_value=description
            ) + "#expenses"
        )

    # VALIDATE AMOUNT TYPE
    # Convert the entered amount to a float and handle invalid input.
    try:
        amount = float(raw_amount)
    except ValueError:
        return redirect(
            url_for(
                "main.dashboard",
                open_modal="edit",
                edit_error="Please enter a valid number.",
                edit_expense_id=expense_id,
                edit_amount_value=raw_amount,
                edit_category_value=category_id,
                edit_date_value=date,
                edit_description_value=description
            ) + "#expenses"
        )

    # VALIDATE POSITIVE AMOUNT
    # The amount must be greater than zero.
    if amount <= 0:
        return redirect(
            url_for(
                "main.dashboard",
                open_modal="edit",
                edit_error="Amount must be greater than zero.",
                edit_expense_id=expense_id,
                edit_amount_value=raw_amount,
                edit_category_value=category_id,
                edit_date_value=date,
                edit_description_value=description
            ) + "#expenses"
        )

    # VALIDATE DATE
    # Ensure a date has been selected.
    if date == "":
        return redirect(
            url_for(
                "main.dashboard",
                open_modal="edit",
                edit_error="Please choose a date.",
                edit_expense_id=expense_id,
                edit_amount_value=raw_amount,
                edit_category_value=category_id,
                edit_date_value=date,
                edit_description_value=description
            ) + "#expenses"
        )

    # VALIDATE CATEGORY
    # Ensure a category has been selected.
    if category_id == "":
        return redirect(
            url_for(
                "main.dashboard",
                open_modal="edit",
                edit_error="Please choose a category.",
                edit_expense_id=expense_id,
                edit_amount_value=raw_amount,
                edit_category_value=category_id,
                edit_date_value=date,
                edit_description_value=description
            ) + "#expenses"
        )

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