"""
tracker/routes/dashboard/export_csv.py
-------------------------------------
This file creates a route that lets the logged-in user
download all of their expenses as a CSV file.
"""

# csv helps us build CSV files in Python.
import csv

# io lets us create a file in memory instead of saving it on disk.
import io

# Response sends the CSV file back to the browser.
# redirect and url_for are used if the user is not logged in.
# session lets us know which user is logged in.
from flask import Response, redirect, session, url_for

# Import the database helper function so we can read expenses.
from ...models import get_db_connection

# Import the shared Blueprint used by your app routes.
from ..main_blueprint import main


# Create a new route.
# When the user visits /export-csv, this function will run.
@main.route("/export-csv")
def export_csv() -> Response:
    """
    Export the logged-in user's expenses as a CSV file.
    """

    # STEP 1: Check if the user is logged in.
    # If there is no user_id in the session, send them to the login page.
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # STEP 2: Open the database connection.
    conn = get_db_connection()
    cursor = conn.cursor()

    # STEP 3: Get this user's expenses from the database.
    # We also join the categories table so we can show category names
    # instead of only category IDs.
    expenses = cursor.execute(
        """
        SELECT expenses.date, categories.name, expenses.amount, expenses.description
        FROM expenses
        JOIN categories ON expenses.category_id = categories.category_id
        WHERE expenses.user_id = ?
        ORDER BY expenses.date DESC
        """,
        (session["user_id"],)
    ).fetchall()

    # STEP 4: Close the database connection.
    conn.close()

    # STEP 5: Create an in-memory text file.
    # This lets us build the CSV content without creating a real file on disk.
    output = io.StringIO()

    # STEP 6: Create a CSV writer.
    writer = csv.writer(output)

    # STEP 7: Write the first row (the column headings).
    writer.writerow(["Date", "Category", "Amount", "Description"])

    # STEP 8: Write one row for each expense.
    for expense in expenses:
        writer.writerow([
            expense["date"],                 # The expense date
            expense["name"],                 # The category name
            expense["amount"],               # The amount spent
            expense["description"] or ""     # Description, or blank if empty
        ])

    # STEP 9: Get all the CSV text from memory.
    csv_data = output.getvalue()

    # STEP 10: Close the memory file.
    output.close()

    # STEP 11: Send the CSV file to the browser.
    # The browser will download it as "expenses.csv".
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=expenses.csv"
        }
    )