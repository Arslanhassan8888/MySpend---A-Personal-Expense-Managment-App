## 21/02/2026 – Architectural Planning

Today I implemented a modular Flask project structure using a package-based design.
Instead of placing all logic in a single file, I separated the application into:
- Entry point (app.py)
- Application package (tracker/)
- Database models (models.py)
- Route handling (routes.py)

This approach follows separation of concerns principles and aligns with Flask best practices such as the Application Factory pattern. 

The structure was chosen to ensure scalability, maintainability, and professional development standards.

## 24/03/2026 – Environment Setup
I installed the core backend dependencies for the MySpend project.

Flask was installed as the main web framework, and Flask-SQLAlchemy was added to manage database interactions using an ORM approach.

All dependencies were documented in requirements.txt to ensure reproducibility and professional project structure.

## 27/03/2026 – Database Approach Revision
After reviewing project complexity and personal skill level, I decided to simplify the backend by removing SQLAlchemy and implementing direct SQLite queries using Python’s sqlite3 module.

This decision was made to improve clarity, maintain control over database logic, and strengthen foundational SQL understanding. The project dependencies were updated accordingly, and the repository was synchronised with GitHub.

This change maintains professional structure while ensuring the system remains manageable within the project timeframe.

## 04/03/2026 – Refactoring to Modular Structure
Today I refactored the Flask application from a single-file structure to a modular architecture. I implemented the Application Factory pattern and organised routes using a Blueprint. This improves code organisation, scalability, and maintainability. The application was tested and runs successfully in modular format.

## 05/03/2026 - HTML Template Integration
I connected the Flask backend to a frontend HTML template using render_template(). I created a templates folder and added an index.html file for the home page. This step allowed the application to return a structured webpage instead of plain text. The integration was tested successfully and the page renders correctly in the browser.


## 09/03/2026 – SQLite Database Connection
Implemented the initial SQLite database connection using Python’s sqlite3 module. The connection function was added in models.py and integrated into the Flask Application Factory.

An import error occurred during testing. The issue was resolved by deleting Python cache files (__pycache__) and restarting Visual Studio Code.

After fixing the environment issue, the application ran successfully and the database file (myspend.db) was created.

## 10/03/2026 Part A- Database Schema Implementation
Implemented the SQLite database schema for the MySpend application. The database tables were created using SQL queries inside models.py, representing the core entities of the system including users, expenses, income, budgets, goals, recurring expenses, and categories.

The table creation process was integrated into the Flask Application Factory so that the database schema is automatically initialized when the application starts. This ensures that the system can create and manage persistent financial data without requiring manual database setup.

## 10/03/2026 Part B – Default Categories Initialization
Implemented automatic insertion of predefined spending categories into the database. A function was added in models.py to insert default categories such as Food, Transport, Entertainment, Rent, Utilities, Shopping, Health, Education, and Other.

This function is executed when the Flask application starts, ensuring that the categories table always contains the required options for expense classification. The categories are inserted using `INSERT OR IGNORE` to prevent duplicate entries if the application restarts.

The changes were committed to the repository after verifying that the database correctly creates the categories when the application is launched.

## 11/03/2026 – User Registration Implementation
Implemented the user registration functionality in the MySpend application. A new /register route was created in routes.py to display the registration page and process form submissions. The Flask request object was used to retrieve the email and password values from the HTML form.

Password security was implemented using generate_password_hash from the werkzeug.security module to store passwords as secure hashes instead of plain text.

A new template page register.html was created to provide the registration interface. Jinja templating was used to display an error message when a user attempts to register with an email that already exists in the database. This prevents duplicate accounts and improves user feedback.

The redirect and url_for functions were used to navigate the user back to the home page after successful registration. The feature was tested successfully by verifying both normal registration and duplicate email handling.

## 11/03/2026 – Login and Session Implementation
Implemented the user login functionality by creating a /login route and a new login.html template. I used Flask’s request object to retrieve the email and password from the form and verified the credentials using check_password_hash.

I also introduced session management using Flask’s session object. After successful authentication, I stored the user’s user_id in the session to keep the user logged in. Basic error handling was added to display a message when invalid login credentials are entered.

## 12/03/2026 – Registration Improvements and Login Security
Improved the registration system by adding a name field to the registration form and updating the users table to store this information. I also created a registration success page (register_success.html) to confirm that the account was created before the user proceeds to login.

Additionally, I implemented a login security feature that limits users to three failed login attempts. If the password is entered incorrectly three times, the account is locked for 15 minutes using the lockout_until field in the database.

During development I encountered an issue where login stopped working due to a database schema error (a missing comma in the users table definition). After correcting the schema and recreating the database, the login system functioned correctly.

## 15/03/2026 – Dashboard Implementation and Access Control
I implemented the first version of the dashboard page to display a welcome message and navigation links for the user area. During testing I discovered that the dashboard route assumed a valid session always existed. When accessing /dashboard without logging in, the application attempted to read session["user_id"], which could cause an error. I solved this by adding a session validation check that redirects unauthenticated users to the login page.

## 16/03/2026 – Debugging Add Expense Feature
During testing of the expense submission form,
the application raised a Flask BadRequestKeyError.

Investigation of the traceback revealed that the add_expense() route attempted to access request.form["category"] while the HTML form
used the field name "category_id".

After verifying the mismatch between the backend route and frontend form, the issue was resolved by correcting the field name in routes.py.

## 18/03/2026 – Editing and Sorting Features
I implemented an edit functionality that allows users to update expenses through a modal interface, improving usability and avoiding unnecessary page navigation.
I also added a sorting system to help users organise expenses by date, amount, category, and description. Initially, I attempted to use sorting arrows in the table headers, but this caused HTML rendering issues and was not user-friendly.

While implementing sorting, I encountered errors in the SQL query due to incorrect string formatting when applying the dynamic ORDER BY clause. I resolved this by using a properly structured f-string.
I then redesigned the feature using a modal-based sorting interface, which provides a clearer and more structured user experience. Both features were tested successfully and improved the overall functionality of the dashboard.

## 19/03/2026 – Search and Filter Features
I implemented a search and filtering functionality using a modal interface, allowing users to find expenses based on date range, amount range, and description. This improved usability by enabling quicker access to specific data without navigating away from the dashboard.

Initially, the search feature did not work correctly, as all expenses were still displayed even when filters were applied. This was due to the SQL query being static and not including the filtering conditions.
I resolved this by modifying the query to dynamically add conditions only when input values were provided, using request arguments and parameterised queries.

I also added a clear button to reset all filters and restore the full list. 