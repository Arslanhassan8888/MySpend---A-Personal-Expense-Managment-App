"""
tracker/routes/dashboard/dashboard_page.py
-----------------------------------------
This file contains the main dashboard page route for the MySpend application.
"""

# render_template is used to render HTML templates.
# request is used to access values from the URL, such as sorting and search filters.
# redirect and url_for are used to move users to another page when needed.
from flask import render_template, request, redirect, url_for

# session is used to check if the user is logged in.
from flask import session

# datetime is used to work with the current month and date values.
from datetime import datetime, timedelta

# flash is used to display messages to the user.
from flask import flash

# Import the database connection helper from models.py.
from ...models import get_db_connection

# Import the shared Blueprint.
from ..main_blueprint import main


# Dashboard route - shows user-specific financial information after login
@main.route("/dashboard")
def dashboard() -> str:
    """
    Display the main dashboard page.

    This route:
    - checks whether the user is logged in
    - loads the user's details
    - applies sorting and search filters to expenses
    - calculates totals for spending and budget
    - sends all dashboard data to the template

    Returns:
        str: Rendered HTML page or redirect response
    """

    # Check whether the user is logged in before showing the dashboard
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the user's name using the user_id stored in the session
    user = cursor.execute(
        "SELECT name FROM users WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()
    
    # If the user record no longer exists, clear the session and redirect to login
    if user is None:
        conn.close()
        session.clear()
        flash("Your session has expired. Please log in again.", "error")
        return redirect(url_for("main.login"))

    # SORT
    # Get the selected sort option from the URL query string.
    # If nothing is chosen, use newest date first as the default.
    raw_sort = request.args.get("sort")  # Store the original sort value from the URL before applying any default.

    sort = raw_sort
    if not sort: # If no sort option is provided in the URL, we set the default
        sort = "date_desc" # Default sorting is by date descending (newest first)
    # Match the selected sort key to the correct SQL ORDER BY clause.
    order_clause = {
        "date_desc": "expenses.date DESC", # Sort by date descending (newest first)
        "date_asc": "expenses.date ASC", # Sort by date ascending (oldest first)
        "amount_asc": "expenses.amount ASC", # Sort by amount ascending (lowest first)
        "amount_desc": "expenses.amount DESC", # Sort by amount descending (highest first)
        "category_asc": "categories.name ASC", # Sort by category name ascending (A-Z)
        "category_desc": "categories.name DESC", # Sort by category name descending (Z-A)
        "desc_asc": "expenses.description ASC", # Sort by description ascending (A-Z)
        "desc_desc": "expenses.description DESC" # Sort by description descending (Z-A)
    }.get(sort, "expenses.date DESC") # Use the provided sort key to get the corresponding ORDER BY clause, or default to "expenses.date DESC" if the key is not recognized.

    # SEARCH FILTERS
    # Read optional filter values from the URL query string.
    date_from = request.args.get("date_from")   # Get the "date_from" filter value from the URL query string, which represents the start date for filtering expenses. If the user has entered a date in the filter form, it will be included in the URL as a query parameter (e.g., ?date_from=2024-01-01). If no value is provided, this will be None.
    date_to = request.args.get("date_to")      
    min_amount = request.args.get("min_amount") 
    max_amount = request.args.get("max_amount")    
    description = request.args.get("description") 
    category_id = request.args.get("category_id")   
    
    # MODAL CONTROL AND SERVER-SIDE VALIDATION MESSAGES
    # These values allow Flask to reopen a modal after redirect
    # and display any validation errors inside it.
    open_modal = request.args.get("open_modal", "")   # Get the "open_modal" value from the URL query string, which indicates which modal should be reopened after a redirect. If no value is provided, this will be an empty string.
    sort_error = request.args.get("sort_error", "")   
    search_error = request.args.get("search_error", "") 
    edit_error = request.args.get("edit_error", "")   

    # EDIT MODAL FIELD VALUES
    # These values are used to refill the edit modal form
    # if validation fails after submission.
    edit_expense_id = request.args.get("edit_expense_id", "")
    edit_amount_value = request.args.get("edit_amount_value", "")
    edit_category_value = request.args.get("edit_category_value", "")
    edit_date_value = request.args.get("edit_date_value", "")
    edit_description_value = request.args.get("edit_description_value", "")
    
    # SEARCH VALIDATION
    # Validate search input values before applying filters.
    # If validation fails, redirect back and reopen the search modal with an error.

    # VALIDATE AMOUNT VALUES
    # Check that min and max amounts are valid numbers if provided.
    try: # Attempt to convert the min_amount and max_amount values from the URL query string to floats. If the conversion fails (e.g., if the user entered a non-numeric value), a ValueError will be raised, and we catch that to handle the error gracefully.
        if min_amount: # If a min_amount value is provided in the URL query string (e.g., ?min_amount=10).
                raise ValueError 

        if max_amount:
            max_amount_float = float(max_amount)
            if max_amount_float < 0:
                raise ValueError
    except ValueError:
        return redirect(
            url_for(
                "main.dashboard",
                open_modal="search",
                search_error="Amounts must be valid positive numbers.",
                description=description,
                min_amount=min_amount,
                max_amount=max_amount,
                date_from=date_from,
                date_to=date_to,
                category_id=category_id
            ) + "#expenses"
        )

    # VALIDATE MIN <= MAX
    # Ensure minimum amount is not greater than maximum amount.
    if min_amount and max_amount:
        if float(min_amount) > float(max_amount):
            return redirect(
                url_for(
                    "main.dashboard",
                    open_modal="search",
                    search_error="Minimum amount cannot be greater than maximum amount.",
                    description=description,
                    min_amount=min_amount,
                    max_amount=max_amount,
                    date_from=date_from,
                    date_to=date_to,
                    category_id=category_id
                ) + "#expenses"
            )

    # VALIDATE DATE RANGE
    # Ensure the start date is not after the end date.
    if date_from and date_to:
        if date_from > date_to:
            return redirect(
                url_for(
                    "main.dashboard",
                    open_modal="search",
                    search_error="Start date cannot be after end date.",
                    description=description,
                    min_amount=min_amount,
                    max_amount=max_amount,
                    date_from=date_from,
                    date_to=date_to,
                    category_id=category_id
                ) + "#expenses"
            )

    # SORT VALIDATION
    # If the sort modal was submitted, require at least one sort option.
    # We check the original submitted sort value, not the default value.
    if open_modal == "sort":
        has_sort_option = raw_sort is not None and raw_sort != ""
        has_category = category_id is not None and category_id != ""

        if not has_sort_option and not has_category:
            return redirect(
                url_for(
                    "main.dashboard",
                    open_modal="sort",
                    sort_error="Please choose a sort option or select a category before applying.",
                    category_id=category_id
                ) + "#expenses"
            )
    
    
    # BASE QUERY
    # Start with the main query to load this user's expenses,
    # joined with categories so the category name can also be shown.
    
    query = f"""
    SELECT expenses.expense_id, expenses.date, expenses.amount, expenses.description, categories.name, expenses.category_id
    FROM expenses
    JOIN categories ON expenses.category_id = categories.category_id
    WHERE expenses.user_id = ?
    """

    # Start the parameter list with the logged-in user's ID.
    params = [session["user_id"]]

    # APPLY FILTERS
    # Add extra conditions only if the user entered values.

    if date_from and date_from != "": # If the user provided a "date_from" value in the URL query string (e.g., ?date_from=2024-01-01), we add a condition to the SQL query to filter expenses with a date greater than or equal to that value. We also append the "date_from" value to the list of parameters that will be passed to the query execution.
        query += " AND expenses.date >= ?" # Add a condition to the SQL query to filter expenses with a date greater than or equal to the "date_from" value.
        params.append(date_from) # Append the "date_from" value to the list of parameters for the query execution.

    if date_to and date_to != "": # If the user provided a "date_to" value in the URL query string (e.g., ?date_to=2024-01-31), we add a condition to the SQL query to filter expenses with a date less than or equal to that value. We also append the "date_to" value to the list of parameters that will be passed to the query execution.
        query += " AND expenses.date <= ?" # Add a condition to the SQL query to filter expenses with a date less than or equal to the "date_to" value.
        params.append(date_to) # Append the "date_to" value to the list of parameters for the query execution.

    if min_amount and min_amount != "":
        query += " AND expenses.amount >= ?"
        params.append(min_amount)

    if max_amount and max_amount != "":
        query += " AND expenses.amount <= ?"
        params.append(max_amount)

    if description and description != "":
        query += " AND expenses.description LIKE ?"
        params.append(f"%{description}%")
        
    if category_id and category_id != "":
        query += " AND expenses.category_id = ?"
        params.append(category_id)

    # SORT
    # Add the final ORDER BY part to the SQL query.
    query += f" ORDER BY {order_clause}"

    # EXECUTE
    # Run the completed query and fetch the filtered expense list.
    expenses = cursor.execute(query, params).fetchall() # Execute the SQL query with the constructed query string and the list of parameters, which includes the user_id and any filter values provided by the user. The result is a list of expenses that match the filters and are sorted according to the selected sort option.

    # TOTAL
    # Calculate the user's total spending across all expenses.
    total = cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]

    # MONTHLY TOTAL
    # Calculate total spending for the current month only.
    monthly_total = cursor.execute( # We execute a SQL query to calculate the total amount of expenses for the logged-in user for the current month. We use COALESCE to return 0 if there are no expenses, and we filter expenses by user_id and the current month using strftime to extract the year and month from the date field.
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """,
        (session["user_id"],)
    ).fetchone()[0]
    
    # Get the current month in YYYY-MM format for the budget lookup.
    month = datetime.now().strftime("%Y-%m")

    # Get the budget set for the current month.
    budget = cursor.execute("""
        SELECT amount FROM budgets
        WHERE user_id = ? AND month = ?
    """, (session["user_id"], month)).fetchone()

    # Use the saved budget amount if it exists, otherwise use 0.
    budget_amount = budget[0] if budget else 0

    # Calculate how much budget is left after current monthly spending.
    remaining = budget_amount - monthly_total

    # Calculate the budget progress percentage.
    # If no budget has been set, use 0 to avoid division by zero.
    if budget_amount > 0:
        progress = (monthly_total / budget_amount) * 100
    else:
        progress = 0
        
    # DAILY TOTAL
    # Calculate spending for today only.
    daily_total = cursor.execute( # We execute a SQL query to calculate the total amount of expenses for the logged-in user for today. We use COALESCE to return 0 if there are no expenses, and we filter expenses by user_id and today's date using DATE('now').
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND date = DATE('now')
        """,
        (session["user_id"],)
    ).fetchone()[0]

    # WEEKLY TOTAL
    # Calculate spending for the current week range.
    weekly_total = cursor.execute( # We execute a SQL query to calculate the total amount of expenses for the logged-in user for the current week. We use COALESCE to return 0 if there are no expenses, and we filter expenses by user_id and the current week using DATE and weekday functions.
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
         AND date BETWEEN DATE('now', 'weekday 1', '-7 days')
                  AND DATE('now', 'weekday 0')
        """,
        (session["user_id"],)
    ).fetchone()[0]

    # Get all categories so they can be shown in forms and filters.
    categories = cursor.execute( # We execute a SQL query to fetch all categories from the database. This allows us to display them in forms and filters on the dashboard.
        "SELECT * FROM categories"
    ).fetchall()

    # Close the database connection
    conn.close()

    # Render the dashboard page with all required data
    return render_template(
        "dashboard.html",
        name=user["name"],
        expenses=expenses,
        total=total,
        monthly_total=monthly_total,
        daily_total=daily_total,
        weekly_total=weekly_total,
        categories=categories,
        budget_amount=budget_amount,
        remaining=remaining,
        progress=progress,
        current_month=datetime.now().strftime("%B %Y"),
        open_modal=open_modal,
        sort_error=sort_error,
        search_error=search_error,
        edit_error=edit_error,
        edit_expense_id=edit_expense_id,
        edit_amount_value=edit_amount_value,
        edit_category_value=edit_category_value,
        edit_date_value=edit_date_value,
        edit_description_value=edit_description_value
    )
    