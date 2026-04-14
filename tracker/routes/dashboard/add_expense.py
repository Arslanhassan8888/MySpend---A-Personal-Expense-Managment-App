"""
tracker/routes/dashboard/add_expense.py
--------------------------------------
This file contains the add expense route for the MySpend application.
"""

# request is used to access form data sent by the user.
# redirect and url_for are used to navigate after actions (e.g. form submission).
from flask import request, redirect, url_for

# session is used to check if the user is logged in.
from flask import session

# flash is used to display messages to the user (success or error).
from flask import flash

# Import the database connection helper from models.py.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


@main.route("/add-expense", methods=["POST"])
def add_expense() -> str:
    """
    Handle adding a new expense.

    This route:
    - checks that the user is logged in
    - validates the input (especially the amount)
    - inserts the expense into the database
    - redirects back to the dashboard with a message

    Returns:
        str: Redirect response
    """

    # Check if the user is logged in before allowing access
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # This route only handles POST requests (form submission)
    if request.method == "POST":

        # Validate the amount entered by the user
        try:
            amount = float(request.form["amount"])

            # Ensure the amount is greater than zero
            if amount <= 0:
                flash("Amount must be greater than zero.")
                return redirect(url_for("main.dashboard") + "#expenses")

        except ValueError:
            # Handle cases where the input is not a valid number
            flash("Invalid amount. Please enter a valid number.")
            return redirect(url_for("main.dashboard") + "#expenses")

        # Retrieve other form values
        category_id = request.form["category_id"]
        date = request.form["date"]
        description = request.form["description"].strip()

        # Connect to the database and insert the new expense
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (user_id, category_id, date, amount, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],  # Link expense to the logged-in user
                category_id,
                date,
                amount,
                description
            )
        )

        # Save changes and close connection
        conn.commit()
        conn.close()

        # Show success message and redirect to dashboard
        flash("Expense added successfully!", "success")
        return redirect(url_for("main.dashboard") + "#add-expense")