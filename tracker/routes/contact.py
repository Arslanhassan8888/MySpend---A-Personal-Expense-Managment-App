"""
tracker/routes/contact.py

This file contains the contact page route for the MySpend application.
"""

# render_template is used to render HTML templates.
# request is used to access form data sent by the user.
# redirect and url_for are used to redirect users to different pages after certain actions.
from flask import render_template, request, redirect, url_for

# Import flash for displaying messages to users (e.g., success or error messages)
from flask import flash

# Import the shared Blueprint.
from .main_blueprint import main


# Route for the contact page.
# This page displays the contact form and handles message submission.
@main.route("/contact", methods=["GET", "POST"])
def contact():

    # Show the page normally
    if request.method == "GET":
        return render_template("contact.html")

    # Get submitted form values and remove extra spaces
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    # Validate that all fields are filled in
    if not full_name or not email or not subject or not message:
        return render_template(
            "contact.html",
            error="All fields are required.",
            entered_name=full_name,
            entered_email=email,
            entered_subject=subject,
            entered_message=message
        )

    # Validate email format
    if "@" not in email or "." not in email:
        return render_template(
            "contact.html",
            error="Please enter a valid email address.",
            entered_name=full_name,
            entered_email=email,
            entered_subject=subject,
            entered_message=message
        )

    # Show success message once and clear form
    flash("Thank you for contacting MySpend. Your message has been sent successfully.", "success")
    return redirect(url_for("main.contact"))