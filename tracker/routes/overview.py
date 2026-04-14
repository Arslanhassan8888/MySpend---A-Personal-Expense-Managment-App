"""
tracker/routes/overview.py
-------------------------
This file defines the overview route for the MySpend application.

The page shows spending trends using chart data for:
- daily spending
- weekly spending
- monthly spending
- category totals for the current month
"""

# render_template is used to display HTML pages.
# redirect and url_for are used to move users to another route when needed.
from flask import render_template, redirect, url_for

# session is used to check whether the user is logged in.
from flask import session

# flash is used to show messages to the user.
from flask import flash

# datetime and timedelta are used to calculate dates and date ranges.
from datetime import datetime, timedelta

# Import the database connection helper.
from ..models import get_db_connection

# Import the shared Blueprint.
from .main_blueprint import main


# STEP 1: Overview page route
@main.route("/overview")
def overview() -> str:
    """
    Display the overview page with chart data.

    This route:
    - checks whether the user is logged in
    - loads the user's name from the database
    - prepares daily, weekly, monthly, and category chart data
    - sends that data to the overview template

    Returns:
        str: Rendered HTML page or redirect response
    """

    # Check whether the user is logged in
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Open database connection and create cursor
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the user's name for display on the page
    user = cursor.execute(
        "SELECT name FROM users WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    # If the user no longer exists, clear the session and send them back to login
    if user is None:
        conn.close()
        session.clear()
        flash("Your session has expired. Please log in again.", "error")
        return redirect(url_for("main.login"))

    # STEP 2: Prepare daily chart data
    # These lists will store the day labels and daily totals for the last 7 days.
    daily_labels = []
    daily_values = []

    today = datetime.now().date() # Get today's date to calculate the last 7 days. We use .date() to work with date objects instead of datetime.

    # Loop through the last 7 days, from oldest to newest
    for i in range(6, -1, -1): # We loop from 6 down to 0 to get the last 7 days in order from oldest to newest. For example, if today is the 7th, we will calculate for the 1st (6 days ago), then the 2nd (5 days ago), and so on until the 7th (0 days ago).
        day = today - timedelta(days=i) # Calculate the date for this day by subtracting i days from today. This gives us the date for each of the last 7 days.
        day_name = day.strftime("%a") # Get the abbreviated weekday name (e.g., "Mon", "Tue") for this date to use as a label on the chart.

        # Get the total spending for this day
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ? AND date = ?
            """,
            (session["user_id"], day.isoformat()) # We use day.isoformat() to convert the date to a string in "YYYY-MM-DD" format, which matches how dates are stored in the database.
        ).fetchone()[0]

        # If no expenses exist for that day, use 0
        if result is None:
            result = 0

        daily_labels.append(day_name)
        daily_values.append(float(result))

    # STEP 3: Prepare weekly chart data
    # These lists store totals for the last 4 weeks.
    weekly_labels = []
    weekly_values = []

    today = datetime.now().date() # Get today's date to calculate the last 4 weeks. We use .date() to work with date objects since our expenses are stored with date precision.

    # Loop through the last 4 weeks, from oldest to newest
    for i in range(3, -1, -1): # We loop from 3 down to 0 to get the last 4 weeks in order from oldest to newest. For example, if today is the 28th, we will calculate for the week starting on the 7th (3 weeks ago), then the week starting on the 14th (2 weeks ago), and soon until the week starting on the 21st (current week).
        days_back_start = (i * 7) + 6 # Calculate how many days back the start of the week is. For example, for i=3 (3 weeks ago), the start of the week is 27 days back (3*7 + 6), and for i=0 (current week), the start of the week is 6 days back (0*7 + 6).
        days_back_end = i * 7 # Calculate how many days back the end of the week is. For example, for i=3 (3 weeks ago), the end of the week is 21 days back (3*7), and for i=0 (current week), the end of the week is 0 days back (0*7).

        week_start = today - timedelta(days=days_back_start) # Calculate the start date of the week by subtracting days_back_start from today.
        week_end = today - timedelta(days=days_back_end) # Calculate the end date of the week by subtracting days_back_end from today.
 
        week_number = 4 - i # Calculate the week number for labeling (Week 1 = current week, Week 4 = 3 weeks ago). 
        week_label = f"Week {week_number}" # Create a label for the week to use on the chart (e.g., "Week 1", "Week 2", etc.).

        # Get the total spending for this 7-day range
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            AND date BETWEEN ? AND ?
            """,
            (session["user_id"], week_start.isoformat(), week_end.isoformat()) # We use week_start.isoformat() and week_end.isoformat() to convert the dates to strings in "YYYY-MM-DD" format, which matches how dates are stored in the database.
        ).fetchone()[0]

        # If no expenses exist in this week, use 0
        if result is None:
            result = 0

        weekly_labels.append(week_label) # Add the week label to the list of labels for the chart.
        weekly_values.append(float(result)) # Add the total spending for this week to the list of values for the chart, converting it to a float for consistency with the charting library.

    # STEP 4: Prepare monthly chart data
    # These lists store totals for each month of the current year.
    monthly_labels = []
    monthly_values = []

    current_year = datetime.now().year # Get the current year to calculate monthly totals for this year. We will loop through all 12 months of the current year to get their totals.

    # Loop through all 12 months
    for month_number in range(1, 13): # Loop from 1 to 12 to represent each month of the year (1=January, 2=February, ..., 12=December).
        month_date = datetime(current_year, month_number, 1) # Create a date object for the first day of this month, which we can use to get the month name and format the year-month string for querying the database.
        month_label = month_date.strftime("%b") # Get the abbreviated month name (e.g., "Jan", "Feb") for labeling the chart.
        year_month = month_date.strftime("%Y-%m") # Format the year and month as "YYYY-MM" for querying the database.

        # Get the total spending for this month
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            AND strftime('%Y-%m', date) = ?
            """,
            (session["user_id"], year_month) # We use strftime('%Y-%m', date) in the SQL query to extract the year and month from the date field in the database, and compare it to the year_month string we created for this month. This allows us to get the total spending for all expenses that occurred in this month.
        ).fetchone()[0]

        # If no expenses exist for this month, use 0
        if result is None: # If the query returns None (which happens when there are no matching expenses), we set result to 0 so that the chart will show 0 spending for that month instead of being empty or causing an error.
            result = 0

        monthly_labels.append(month_label) # Add the month label to the list of labels for the chart.
        monthly_values.append(float(result)) # Add the total spending for this month to the list of values for the chart, converting it to a float for consistency with the charting library.

    # STEP 5: Prepare category pie chart data
    # These lists store spending totals by category for the current month.
    category_labels = []
    category_values = []

    current_year_month = datetime.now().strftime("%Y-%m") # Get the current year and month formatted as "YYYY-MM" to query expenses for the current month when calculating category totals.

    # Get all categories, including those with no spending this month
    # We use a LEFT JOIN to include all categories, and COALESCE to treat NULL totals as 0. We also filter expenses by user_id and the current month using strftime to extract the year and month from the date field.
    category_rows = cursor.execute(
        """
        SELECT categories.name, COALESCE(SUM(expenses.amount), 0) AS total_amount
        FROM categories
        LEFT JOIN expenses
            ON expenses.category_id = categories.category_id
            AND expenses.user_id = ?
            AND strftime('%Y-%m', expenses.date) = ?
        GROUP BY categories.category_id, categories.name
        ORDER BY categories.name ASC
        """,
        (session["user_id"], current_year_month)
    ).fetchall()

    # Add each category name and total to the chart lists
    for row in category_rows: # Loop through the results of the category query, which includes each category name and the total spending for that category in the current month. 
        category_labels.append(row["name"]) # Add the category name to the list of labels for the chart.
        category_values.append(float(row["total_amount"])) # Add the total spending for this category to the list of values for the chart, converting it to a float for consistency with the charting library.

    # Close database connection
    conn.close()

    # STEP 6: Render the overview page with chart data
    return render_template(
        "overview.html",
        name=user["name"],
        daily_labels=daily_labels, # Pass the list of daily labels (e.g., ["Mon", "Tue", "Wed", ...]) to the template for use in the daily spending chart.
        daily_values=daily_values,  # Pass the list of daily values (e.g., [10, 20, 15, ...]) to the template for use in the daily spending chart.
        weekly_labels=weekly_labels, # Pass the list of weekly labels (e.g., ["Week 1", "Week 2", ...]) to the template for use in the weekly spending chart.
        weekly_values=weekly_values,   # Pass the list of weekly values (e.g., [100, 200, ...]) to the template for use in the weekly spending chart.
        monthly_labels=monthly_labels, # Pass the list of monthly labels (e.g., ["Jan", "Feb", ...]) to the template for use in the monthly spending chart.
        monthly_values=monthly_values, # Pass the list of monthly values (e.g., [100, 200, ...]) to the template for use in the monthly spending chart.
        category_labels=category_labels, # Pass the list of category labels (e.g., ["Food", "Transport", ...]) to the template for use in the category spending chart.
        category_values=category_values # Pass the list of category values (e.g., [150, 75, ...]) to the template for use in the category spending chart.
    )