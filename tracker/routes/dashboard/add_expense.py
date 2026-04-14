"""
tracker/routes/dashboard/add_expense.py

This file contains the add expense route for the MySpend application.
"""

# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages after certain actions.
from flask import request, redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import the get_db_connection function from models.py to interact with the database.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


@main.route("/add-expense", methods=["POST"])
def add_expense():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                flash("Amount must be greater than zero.")
                return redirect(url_for("main.dashboard") + "#expenses")
        except ValueError:
            flash("Invalid amount. Please enter a valid number.")
            return redirect(url_for("main.dashboard") + "#expenses")

        category_id = request.form["category_id"]
        date = request.form["date"]
        description = request.form["description"].strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (user_id, category_id, date, amount, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session["user_id"], category_id, date, 
             amount, description)
        )

        conn.commit()
        conn.close()

        flash("Expense added successfully!", "success")  # Flash a success message to the user
        return redirect(url_for("main.dashboard")+ "#add-expense")  # Redirect to the dashboard and scroll to the expenses section