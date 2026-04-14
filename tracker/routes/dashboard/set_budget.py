"""
tracker/routes/dashboard/set_budget.py

This file contains the set budget route for the MySpend application.
"""

# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages.
from flask import request, redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users.
from flask import flash

# Import datetime for handling date operations.
from datetime import datetime

# Import the get_db_connection function from models.py to interact with the database.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


@main.route("/set-budget", methods=["POST"])
def set_budget():

    if "user_id" not in session:
        return redirect(url_for("main.login"))

    raw_amount = request.form.get("budget_amount", "").strip()

    # EMPTY INPUT
    if raw_amount == "":
        flash("Please enter a budget amount.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    # NOT A NUMBER
    try:
        amount = float(raw_amount)
    except ValueError:
        flash("Please enter a valid number.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    # NEGATIVE OR ZERO
    if amount <= 0:
        flash("Budget must be greater than zero.", "error")
        return redirect(url_for("main.dashboard") + "#budget")

    month = datetime.now().strftime("%Y-%m")

    conn = get_db_connection()
    cursor = conn.cursor()

    existing = cursor.execute("""
        SELECT * FROM budgets
        WHERE user_id = ? AND month = ?
    """, (session["user_id"], month)).fetchone()

    if existing:
        cursor.execute("""
            UPDATE budgets
            SET amount = ?
            WHERE user_id = ? AND month = ?
        """, (amount, session["user_id"], month))
    else:
        cursor.execute("""
            INSERT INTO budgets (user_id, amount, month)
            VALUES (?, ?, ?)
        """, (session["user_id"], amount, month))

    conn.commit()
    conn.close()

    flash("Budget set successfully!", "success")
    return redirect(url_for("main.dashboard") + "#budget")