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