"""
tracker/routes/auth/register.py

This file contains the register route for the MySpend application.
"""

# render_template is used to display HTML pages.
# request is used to read form data sent by the user.
from flask import render_template, request

# Import the database connection helper from models.py.
from ...models import get_db_connection

# generate_password_hash is used to securely hash passwords before storing them.
from werkzeug.security import generate_password_hash

# flash is used to display messages to the user.
from flask import flash

# Import the shared Blueprint.
from ..main_blueprint import main


# Register route handles both:
# - displaying the registration page
# - processing the registration form
@main.route("/register", methods=["GET", "POST"])
def register() -> str:
    """
    Handle user registration.

    This route:
    - shows the registration page
    - validates form input
    - checks for existing email
    - validates password rules
    - creates a new user in the database

    Returns:
        str: Rendered HTML page
    """

    # Default values used when the page first loads
    error = None
    entered_name = ""
    entered_email = ""

    # Process the form only when submitted
    if request.method == "POST":

        # Read form input
        # Get the entered name, email, password, and confirmation from the form. Use strip() to remove any leading or trailing whitespace from the name and email fields. 
        # Convert the email to lowercase to ensure consistency when checking for existing users.
        entered_name = request.form.get("name", "").strip()
        entered_email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        agree_terms = request.form.get("agree_terms")

        # REQUIRED FIELDS
        # Ensure all fields are filled
        # Check if any of the required fields (name, email, password, confirm password) are empty after stripping whitespace. 
        # If any field is missing, set an error message and re-render the registration page with the user's input pre-filled.
        if entered_name == "" or entered_email == "" or password == "" or confirm_password == "":
            error = "Please fill in all fields."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # TERMS CHECKBOX
        # Ensure the user agrees to terms
        if not agree_terms:
            error = "You must agree to the Terms of Service and Privacy Policy."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # SIMPLE EMAIL VALIDATION
        # Check basic email format
        if "@" not in entered_email or "." not in entered_email:
            error = "Please enter a valid email address."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # CHECK IF EMAIL ALREADY EXISTS
        existing_user = cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (entered_email,)
        ).fetchone()

        if existing_user:
            conn.close()
            error = "Email already registered."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # PASSWORD MATCH
        # Ensure password and confirmation match
        if password != confirm_password:
            conn.close()
            error = "Passwords do not match."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # PASSWORD RULES
        # Check password strength requirements
        # Ensure the password is at least 12 characters long and contains at least one number and one special character.
        # This helps improve security by enforcing stronger passwords.
        has_number = any(char.isdigit() for char in password)
        has_special = any(not char.isalnum() for char in password)

        if len(password) < 12:
            conn.close()
            error = "Password must be at least 12 characters long."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        if not has_number:
            conn.close()
            error = "Password must contain at least one number."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        if not has_special:
            conn.close()
            error = "Password must contain at least one special character."
            return render_template(
                "register.html",
                error=error,
                entered_name=entered_name,
                entered_email=entered_email
            )

        # HASH PASSWORD
        # Convert password into a secure hash before storing
        password_hash = generate_password_hash(password)

        # INSERT NEW USER
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (entered_name, entered_email, password_hash)
        )

        conn.commit()
        conn.close()

        # SUCCESS MESSAGE
        success = "Registration completed successfully. Redirecting to login page..."

        return render_template(
            "register.html",
            success=success,
            entered_name="",
            entered_email=""
        )

    # Show page on GET request or after validation errors
    return render_template(
        "register.html",
        error=error,
        entered_name=entered_name,
        entered_email=entered_email
    )