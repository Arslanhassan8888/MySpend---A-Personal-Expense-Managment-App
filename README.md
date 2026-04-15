# MySpend – Personal Finance Tracker

MySpend is a full-stack web application built with **Flask** that helps users manage personal finances, track expenses, and monitor budgets through a clean, accessible, and user-friendly interface.

The project was designed with a strong focus on **usability**, **server-side validation**, **session security**, **modular structure**, and **accessibility compliance**.

---

## Demo Account

A default account is available for demonstration purposes.

Use the following credentials to log in and access protected features:

# Email: arslan@gmail.com
# Password: inter801479?

## Overview

MySpend allows users to:

- record and manage expenses
- monitor spending trends over time
- set and track monthly budgets
- sort and search expense history
- Review spending visually through charts
- interact with a structured dashboard with real-time feedback

The application uses **Flask**, **SQLite**, **Jinja2**, **HTML/CSS**, and **JavaScript**, and follows a modular architecture using **Blueprints** and the **Application Factory pattern**.

---

## Installation and Setup

This guide is written clearly so that even a non-developer can follow it.

---
### Install Required Packages

pip install -r requirements.txt

### Run the Application

python app.py

### Open in Your Browser

http://127.0.0.1:5000

### Use a demo account for login

## Email: arslan@gmail.com
## Password: inter801479?

### Dependencies

The application uses the following important packages:

- Flask
- Flask-WTF
- Jinja2
- Werkzeug
- sqlite3 (built into Python)
- Chart.js (frontend chart library)



## Technologies Used

### Backend

* Python
* Flask
* SQLite

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2
- Chart.js

### Tools
- Visual Studio Code
- Git
- GitHub

## Key Features

### Authentication and Security

- user registration with validation
- secure password hashing
- login system with session handling
- account lockout after repeated failed login attempts
- protected routes for restricted pages
- automatic session validation and logout support

### Expense Management

- add new expenses
- edit existing expenses
- delete individual expenses
- delete multiple selected expenses
- assign categories to expenses
- add optional descriptions
- validate amount, date, and category inputs

### Dashboard

- total spending overview
- daily, weekly, and monthly totals
- monthly budget tracking
- remaining balance calculation
- progress bar and budget chart
- live user feedback through flash messages

### Search and Filtering

- search by description
- filter by minimum amount
- filter by maximum amount
- filter by date range
- filter by category
- modal-based search UI
- server-side validation for invalid or empty searches

### Sorting

- sort by newest to oldest
- sort by oldest to newest
- sort by low to high amount
- sort by high to low amount
- optional category-based sorting/filtering
- success and validation messages displayed clearly in the interface

### Financial Overview

- daily spending chart
- weekly spending chart
- monthly spending chart
- category distribution chart
- visual analytics using **Chart.js**

### Reviews System

- logged-in users can leave a review
- star-based rating system
- duplicate review prevention
- review validation and success feedback

### Contact Form

- contact page with structured form
- validation for required fields
- user-friendly success and error messages

---

## Validation and Error Handling

The application includes full **server-side validation** for reliability and security.

### Validation includes:

- empty field checks
- valid amount checks
- positive number checks
- valid date range checks
- required category selection
- duplicate review prevention
- secure login checks
- password rule enforcement during registration

### Error handling includes:

- inline form error messages
- modal validation messages
- redirect protection
- graceful handling of invalid requests
- session expiry detection
- safe fallback behaviour

---

## Flash Message System

The application uses a structured flash message system to improve user experience.

### Flash messages are used for:

- successful login/logout
- successful expense addition
- successful budget updates
- successful deletion/update actions
- search and sort feedback
- validation errors
- authentication warnings

Messages are displayed contextually in the correct page section or modal.

---

## Database

MySpend uses **SQLite** for local data storage.

### Main tables include:

- `users`
- `expenses`
- `categories`
- `budgets`
- `reviews`

### Database features:

- automatic table creation
- default category insertion
- relational links between users and expenses
- structured query filtering and sorting
- monthly budget lookup and tracking

---

## Session Handling

The application uses Flask sessions to securely manage logged-in users.

### Session features:

- stores logged-in user ID and name
- clears the session on logout
- validates session before protected page access
- redirects users safely when not authenticated
- handles invalid or expired sessions

### Protected pages include:

- `Dashboard`
- `Overview`
- `Add Review`

---

## Accessibility

Accessibility testing has been completed and passed using the following tools:

- **W3C Validator**
- **WAVE**
- **AXE DevTools**
- **Google Lighthouse**

### Accessibility features include:

- semantic HTML structure
- keyboard-friendly navigation
- ARIA labels for charts and modal elements
- screen reader support
- accessible form labels
- clear visual states and messaging

---
## Project Structure

```text
tracker/
├── routes/
│   ├── auth/              (login, register, logout)
│   ├── dashboard/         (dashboard actions, sorting, searching, budget, expenses)
│   └── pages/             (general site pages)
│
├── templates/             (Jinja2 HTML templates)
├── static/
│   ├── css/               (stylesheets)
│   ├── js/                (JavaScript files)
│   └── images/            (images, logo, favicon)
│
├── models.py              (database logic)
├── app.py                 (application entry point)
└── myspend.db             (SQLite database)

## Future Improvements

The project can be extended further with more advanced financial features and system integrations.

---

### Income Handling

- Add support for income tracking  
- Calculate net balance using both income and expenses  
- Display savings growth over time  

---

### Banking API Integration

- Connect to external banking APIs  
- Automate transaction importing  
- Reduce manual entry of expenses  
- Support automatic expense categorisation  

---

### Advanced Financial Analytics

- Provide predictive spending insights  
- Enable monthly comparisons  
- Export data to CSV or PDF  
- Generate custom financial reports  

---

### Security Improvements

- Implement two-factor authentication (2FA)  
- Add email verification  
- Provide password reset functionality  
- Improve secret management using environment variables  

---

### UI and UX Improvements

- Improve mobile responsiveness  
- Add dark mode support  
- Introduce advanced user preferences  
- Enhance onboarding experience  

---

## Author

## Arslan Hassan
