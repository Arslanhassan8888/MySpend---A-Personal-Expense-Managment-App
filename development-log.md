## 21/02/2026 – Architectural Planning

Today I implemented a modular Flask project structure using a package-based design.
Instead of placing all logic in a single file, I separated the application into:
- Entry point (app.py)
- Application package (tracker/)
- Database models (models.py)
- Route handling (routes.py)

This approach follows separation of concerns principles and aligns with Flask best practices such as the Application Factory pattern. 

The structure was chosen to ensure scalability, maintainability, and professional development standards.

## 24/02/2026 – Environment Setup
I installed the core backend dependencies for the MySpend project.

Flask was installed as the main web framework, and Flask-SQLAlchemy was added to manage database interactions using an ORM approach.

All dependencies were documented in requirements.txt to ensure reproducibility and professional project structure.

## 27/02/2026 – Database Approach Revision
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

## 20/03/2026 – Budget and Progress Bar
I implemented a monthly budget feature with a progress bar to show spending visually. Users can set a budget, and the system calculates remaining balance and percentage used.

Initially, the progress calculation was incorrect, but I fixed it by using the monthly total divided by the budget. I also added colour indicators (green, yellow, red) to improve usability.

Additionally, I introduced summary cards to display total, monthly, and daily spending more clearly.

## 01/04/2026 – Dashboard Completion and UX Refinement

Today I completed the dashboard by integrating expense creation, editing, deletion, sorting, and filtering into a single page. I implemented modal-based interactions to improve usability and keep the workflow clean without page navigation.

I also refined the user experience by adding anchor-based redirects and flash messages, ensuring actions provide clear feedback and maintain context within the dashboard

## 02/04/2026 – UI Styling and Visual Enhancement

I implemented responsive header navigation with JavaScript-controlled mobile menu and scroll-based transparency effect. Enhanced footer design with structured layout, smooth hover interactions, and consistent styling across all links including policy sections. Applied a refined light purple background theme to improve visual hierarchy and overall user interface quality.

## 04/04/2026 Full style applied on Dasboard page and improved UI and UX
Encountered layout breaking issues on smaller screens due to grid overflow and improper spacing, resolved by applying box-sizing and restructuring responsive CSS. Also faced inconsistent form feedback display, fixed by standardising flash message styling and positioning for better user experience.

## 06/04/2026 Budget Chart Integration
I added a doughnut chart using Chart.js to show monthly spending progress alongside the budget section. I adjusted the styling and layout to match the dashboard design and ensured it updates correctly after any expense or budget change.

## 08/04/2026 Login Page Redesign and UX Improvement

I redesigned the login page with a responsive layout and accessible HTML structure, improving clarity and overall user experience. I implemented clear feedback messages for login errors and successful actions to guide the user more effectively. I also added a show/hide password feature using JavaScript to improve usability during login

## 09/04/2026 Session Protection
"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False
"
HTTPONLY helps stop JavaScript reading the session cookie
SAMESITE="Lax" helps reduce CSRF risk
SECURE=False is correct for local development using normal HTTP

when in future we will deploy in HTTPS we should change to TRUE

## 10/04/2026 – CSRF Protection Implementation

I implemented CSRF protection by installing Flask-WTF and enabling CSRFProtect in the application factory to secure all POST requests. I then updated all active forms to include a hidden CSRF token, ensuring each request is validated before processing.

This improves security by preventing malicious external requests from submitting forms on behalf of authenticated users, protecting sensitive actions such as login, expense management, and budget updates.

## 11/04/2026 Registration Security and UX Improvement

I completed the registration system by applying stronger validation rules, including password confirmation, email formatting, duplicate email checks, and secure password requirements. I also aligned the register page with the login page design and added a delayed success message that redirects the user to the login page after five seconds, improving both usability and consistency.

## 11/04/2026 – Dashboard Modularisation

I refactored the dashboard page to improve structure and maintainability by splitting it into smaller template components.

Previously, all functionality was inside a single large HTML file, which made it difficult to manage and update. I extracted key sections such as the budget, chart, add expense form, expense history, and modals into separate template files using Jinja includes.

During this process, I ensured that all existing functionality remained unchanged, including routes, form actions, CSRF protection, and JavaScript behaviour.

This improvement makes the code easier to read, organise, and extend in the future.

## 12/04/2026 Home Page API Integration (ZenQuotes)

Implemented a dynamic quote system using the ZenQuotes API to display a random motivational message on each visit to the homepage. Created a helper function to handle the API request and added a fallback mechanism to ensure the page always shows a quote if the API fails. Integrated the quote data into the home route and passed it to the template for rendering. Improved reliability by using default values when API fields are missing. Updated the UI to display the quote, author, and source, and enhanced the visual design with a yellow glow border around the quote card.

## 13/04/2026 – Overview Charts Implementation

I implemented dynamic overview charts by extending the /overview route and preparing separate label and value lists for daily, weekly, monthly, and category-based spending data. This required several new SQL aggregation techniques including SUM, BETWEEN, strftime, GROUP BY, COALESCE, and LEFT JOIN to calculate totals correctly and include all categories where needed.

On the frontend, I passed the chart data from Flask into HTML using Jinja tojson inside custom data-* attributes on each canvas. In JavaScript, I used DOMContentLoaded, getElementById, getAttribute, and JSON.parse to retrieve and convert the data before rendering the charts with Chart.js.

I also added chart-specific configuration such as legends, tooltip formatting, axis titles, responsive behaviour, and custom colours. For the category pie chart, I implemented additional JavaScript logic using reduce() and a custom Chart.js plugin to calculate and display percentage labels directly on the chart.