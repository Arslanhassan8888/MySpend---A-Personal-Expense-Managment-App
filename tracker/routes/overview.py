"""
tracker/routes/overview.py

This file contains the overview route for the MySpend application.
"""

# render_template is used to render HTML templates.
# redirect and url_for are used to redirect users to different pages.
from flask import render_template, redirect, url_for

# Import session to manage user sessions (e.g., keeping users logged in).
from flask import session

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import datetime and timedelta for handling date and time operations, such as calculating date ranges for expense tracking.
from datetime import datetime, timedelta

# Import the get_db_connection function from models.py to interact with the database.
from ..models import get_db_connection

# Import the shared Blueprint.
from .main_blueprint import main


@main.route("/overview")
def overview():
    # This route provides an overview of the user's expenses, including daily totals for the past week. It checks if the user is logged in, retrieves the user's name, and then calculates the total expenses for each of the last 7 days. The data is then passed to the overview.html template to be displayed in a chart format.
    # The route first checks if the user is logged in by verifying if "user_id" exists in the session. If not, it redirects the user to the login page. Then it establishes a connection to the database and retrieves the user's name using their user_id from the session. Next, it initializes two lists, daily_labels and daily_values, to store the labels (day names) and corresponding expense totals for each of the last 7 days. It calculates the date for each of the last 7 days, retrieves the total expenses for that day from the database, and appends the results to the respective lists. Finally, it closes the database connection and renders the overview.html template, passing the user's name and the daily labels and values for chart rendering.
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    #open database connection and get user's name to display on the overview page
    conn = get_db_connection()
    cursor = conn.cursor()

    #get the user's name from the database using their user_id stored in the session. This is used to personalize the overview page with a greeting or display the user's name in the header.
    user = cursor.execute(
        "SELECT name FROM users WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()
    
    if user is None:
        conn.close()
        session.clear()
        flash("Your session has expired. Please log in again.", "error")
        return redirect(url_for("main.login"))

    # -----------------------------
    # DAILY CHART DATA
    # -----------------------------
    daily_labels = []
    daily_values = []

    #get the current date and then loop through the last 7 days to calculate the total expenses for each day. For each day, it retrieves the sum of expenses from the database for that specific date and appends the day name (e.g., "Mon", "Tue") to daily_labels and the corresponding total amount to daily_values. This data is then used to render a chart on the overview page that shows the user's spending trends over the past week.
    today = datetime.now().date()

    # Loop through the last 7 days (including today) to get daily totals. The loop starts from 6 and goes down to 0, which allows us to calculate the date for each of the last 7 days by subtracting the appropriate number of days from today's date. For each day, it retrieves the total expenses for that day from the database and appends the results to the daily_labels and daily_values lists.
    for i in range(6, -1, -1):
        # Calculate the date for the current day in the loop by subtracting i days from today's date. This allows us to get the date for each of the last 7 days, starting from 6 days ago up to today. The day_name variable is then set to the abbreviated name of the day (e.g., "Mon", "Tue") using strftime, which is used as a label for the chart.
        day = today - timedelta(days=i)
        #thse labels will be used on the x-axis of the daily expenses chart to indicate which day each data point corresponds to. For example, if today is Wednesday, the labels for the last 7 days would be ["Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed"].
        day_name = day.strftime("%a")

        # Retrieve the total expenses for the current day from the database
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ? AND date = ?
            """,
            (session["user_id"], day.isoformat())
        ).fetchone()[0]

        # If there are no expenses for that day, the result will be None. In that case, we set it to 0 to ensure that the chart displays a value of 0 instead of being empty or showing an error.
        if result is None:
            result = 0

        # Append the day name and total expenses to the respective lists. The day_name is added to daily_labels, which will be used as labels on the x-axis of the chart, while the total expenses (converted to a float) are added to daily_values, which will be used as data points on the y-axis of the chart.
        daily_labels.append(day_name)
        # Convert the result to a float and append it to daily_values. This ensures that the values are in a consistent format for chart rendering, even if the database returns them as integers or None (which we already handled by setting it to 0).
        daily_values.append(float(result))
        
    
    # WEEKLY CHART DATA
    # -----------------------------
       # -----------------------------
    # WEEKLY CHART DATA
    # -----------------------------
    # This section prepares the weekly spending chart data using the same simple
    # Method A structure as the daily chart. We create two separate lists:
    # weekly_labels and weekly_values. The labels will be used on the x-axis of
    # the chart, while the values will be used for the height of the bars.
    # This keeps the code beginner friendly and makes the flow easy to understand:
    # Python prepares the data, the template stores it in HTML data attributes,
    # and JavaScript reads those values to build the chart.
    
    # Create two temporary lists to hold the weekly chart labels and values.
    # The labels will be simple names such as Week 1, Week 2, Week 3, and Week 4.
    # The values will store the total amount spent during each of those weeks.
    weekly_labels = []
    weekly_values = []

    # Get today's date again so we can work backwards through the last 4 weeks.
    # Each week in this chart is a 7 day block, and we will compare the total
    # spending for each of those blocks.
    today = datetime.now().date()

    # Loop through the last 4 weeks, starting from the oldest week and ending
    # with the most recent week. This allows the chart to display in a natural
    # left-to-right order for easier reading.
    for i in range(3, -1, -1):

        # Calculate how many days back the current week starts and ends.
        # Example:
        # i = 3 means the oldest week in the last 4 weeks
        # i = 0 means the most recent week
        days_back_start = (i * 7) + 6
        days_back_end = i * 7

        # Calculate the date range for this 7 day period.
        week_start = today - timedelta(days=days_back_start)
        week_end = today - timedelta(days=days_back_end)

        # Create a simple label for the chart.
        # This keeps the output beginner friendly and easy for the user to read.
        week_number = 4 - i
        week_label = f"Week {week_number}"

        # Query the database to find the total spending during this week range.
        # The BETWEEN clause includes both the start date and end date.
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            AND date BETWEEN ? AND ?
            """,
            (session["user_id"], week_start.isoformat(), week_end.isoformat())
        ).fetchone()[0]

        # If there are no expenses in that week, SQLite returns None.
        # Change it to 0 so the chart can still display correctly.
        if result is None:
            result = 0

        # Add the label and value to the temporary weekly lists.
        weekly_labels.append(week_label)
        weekly_values.append(float(result))

        # -----------------------------
    # MONTHLY CHART DATA
    # -----------------------------
    # This section prepares the monthly spending chart data using the same simple
    # Method A structure as the daily and weekly charts. We create two separate
    # lists called monthly_labels and monthly_values. The labels will be the month
    # names from January to December, and the values will be the total spending
    # for each month in the current year. This keeps the flow clear and easy to
    # follow: Python prepares the data, the template stores it in HTML data
    # attributes, and JavaScript reads the values to build the chart.

    # Create two empty lists to hold the month names and the matching totals.
    monthly_labels = []
    monthly_values = []

    # Get the current year so the chart only shows data for this year.
    # For example, if the current year is 2026, the chart will compare
    # spending from January 2026 to December 2026.
    current_year = datetime.now().year

    # Loop through all 12 months of the year.
    # The loop starts at 1 for January and ends at 12 for December.
    for month_number in range(1, 13):

        # Create a date object for the first day of the current month in the loop.
        # This is used to create a short month label such as Jan, Feb, Mar, and so on.
        month_date = datetime(current_year, month_number, 1)
        month_label = month_date.strftime("%b")

        # Create a year-month string in the format YYYY-MM.
        # This matches the format used by SQLite with strftime('%Y-%m', date).
        # Example: "2026-01" for January 2026.
        year_month = month_date.strftime("%Y-%m")

        # Query the database to find the total amount spent during this month.
        # The query adds together all expense amounts for the logged-in user
        # where the expense date falls inside the current month of the current year.
        result = cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            AND strftime('%Y-%m', date) = ?
            """,
            (session["user_id"], year_month)
        ).fetchone()[0]

        # If there are no expenses for that month, SQLite returns None.
        # Change it to 0 so the chart can still display an empty month correctly.
        if result is None:
            result = 0

        # Add the short month label and the total amount to the two lists.
        # The month label will be used on the x-axis, and the total value
        # will be used on the y-axis of the monthly chart.
        monthly_labels.append(month_label)
        monthly_values.append(float(result))
    
        # -----------------------------
    # CATEGORY PIE CHART DATA
    # -----------------------------
    # This section prepares the category pie chart data using the same simple
    # Method A structure as the other charts. We create two separate lists:
    # category_labels and category_values. The labels will contain the category
    # names, and the values will contain the total amount spent in each category
    # for the current month. This allows the pie chart to show how the user's
    # spending is divided across categories during the current month.

    # Create two empty lists to hold the category names and the matching totals.
    category_labels = []
    category_values = []

    # Create a year-month value for the current month.
    # This allows us to only include expenses from the current month
    # when building the category breakdown.
    current_year_month = datetime.now().strftime("%Y-%m")

       # Query the database to get all categories, even if some categories have
    # no expenses in the current month. We use a LEFT JOIN so every category
    # from the categories table is still returned. If a category has no matching
    # expense in the current month, its total will become 0.
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

    # Loop through the query results and place each category name and total
    # into the matching lists. These lists will later be passed into the
    # overview template and used by JavaScript to build the pie chart.
    for row in category_rows:
        category_labels.append(row["name"])
        category_values.append(float(row["total_amount"]))

    conn.close()
    # Send the chart data to the overview.html template.
    # The template will use daily_labels and daily_values for the daily line chart,
    # weekly_labels and weekly_values for the weekly bar chart,
    # monthly_labels and monthly_values for the monthly line chart,
    # and category_labels and category_values for the category pie chart.
    # The user's name is also passed so the page can remain personalised.
    return render_template(
        "overview.html",
        name=user["name"],
        daily_labels=daily_labels,
        daily_values=daily_values,
        weekly_labels=weekly_labels,
        weekly_values=weekly_values,
        monthly_labels=monthly_labels,
        monthly_values=monthly_values,
        category_labels=category_labels,
        category_values=category_values
    )