from flask import Flask
# This file is the entry point of the application.
#Flask() creates an instance of the Flask class.__name__ is a special variable that holds the name of the current module.
#__name__ is used to determine the root path of the application, which helps Flask locate resources like templates and static files.
#app is the Flask application instance that we will use to define routes and run the server.
app = Flask(__name__)

# Define a route for the home page, and the fucntion below will be executed when the user visits the home page.
@app.route("/")
def home():
    return "Welcome to MySpend"

# The following code checks if the script is being run directly (as the main program) and not imported as a module in another script.
if __name__ == "__main__":
    app.run(debug=True) # This starts the Flask development server. debug=True enables debug mode, which provides detailed error messages and auto-reloads the server when code changes are detected. This is useful during development but should be turned off in production for security reasons.