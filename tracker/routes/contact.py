"""
tracker/routes/contact.py
------------------------
This file defines the route for the Contact page.

Users can submit a message through a form.
The input is validated before showing a success message.
"""

# render_template displays HTML pages.
# request is used to access form data.
# redirect and url_for are used for navigation after submission.
from flask import render_template, request, redirect, url_for

# flash is used to display messages to the user.
from flask import flash

# Import the shared Blueprint.
from .main_blueprint import main


# STEP 1: Contact page route
@main.route("/contact", methods=["GET", "POST"])
def contact() -> str:
    """
    Handle the contact page.

    This route:
    - displays the contact form
    - processes submitted form data
    - validates user input
    - shows a success message after submission

    Returns:
        str: Rendered HTML page or redirect response
    """

    # STEP 2: Display page on normal load
    # When the user first visits the contact page, they will see the form. This is handled by checking if the request method is GET and rendering the contact.html template.
    if request.method == "GET":
        return render_template("contact.html")

    # STEP 3: Get form data and clean input
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    # STEP 4: Validate required fields
    if not full_name or not email or not subject or not message: # Check if any of the required fields are empty after stripping whitespace. If any field is missing, re-render the form with an error message and pre-fill the fields with the user's input.
        return render_template(
            "contact.html",
            error="All fields are required.",
            entered_name=full_name,
            entered_email=email,
            entered_subject=subject,
            entered_message=message
        )

    # Validate email format (basic check)
    if "@" not in email or "." not in email: # This is a very basic validation to check if the email contains "@" and "." characters. For a production application, consider using a more robust email validation method or library. If the email format is invalid, re-render the form with an error message and pre-fill the fields with the user's input.
        return render_template(
            "contact.html",
            error="Please enter a valid email address.",
            entered_name=full_name,
            entered_email=email,
            entered_subject=subject,
            entered_message=message
        )

    # STEP 5: Show success message and reload page
    # After successfully validating the form data, display a success message to the user using flash and redirect them back to the contact page.
    flash("Thank you for contacting MySpend. Your message has been sent successfully.", "success")

    return redirect(url_for("main.contact"))