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
