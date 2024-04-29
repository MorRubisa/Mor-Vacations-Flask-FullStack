from flask import Flask, render_template
from views.home_view import home_blueprint
from views.vacations_view import vacations_blueprint
from views.auth_view import auth_blueprint
from logging import getLogger, ERROR
from utils.app_config import AppConfig


# Creating Flask server:
app = Flask(__name__)

# Registering all routes: 
app.register_blueprint(auth_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(vacations_blueprint)

# Catch any 404 route: 
@app.errorhandler(404)
def page_not_found (error):# error = an object containing details about the 404 error. 
    return render_template ("404.html")

# Catch any unhandled exception error:
@app.errorhandler(Exception)
def catch_all(error):
    print(error)
    return render_template("500.html", error=error)

# Create session secret key: 
app.secret_key = AppConfig.session_secret_key

# Quiet console (werkzeug = ארגז כלים): 
getLogger("werkzeug").setLevel(ERROR)

# Display website address on terminal: Website is at: http://localhost:5000/ http://127.0.0.1:5000/
print("http://localhost:5000")