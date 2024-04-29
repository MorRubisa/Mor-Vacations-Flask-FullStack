from flask import Blueprint, render_template, send_file, redirect, url_for, request, session, flash
from facades.vacations_facade import VacationsFacade
from facades.auth_facade import AuthFacade
from facades.user_facade import UserFacade
from utils.image_handler import ImageHandler
from models.client_errors import ResourceNotFoundError, ValidationError, AuthError

# Managing the entire view
vacations_blueprint = Blueprint("vacations_view", __name__) # "vacations_view" is the name of the view

# Create facades: 
vacations_facade = VacationsFacade()
auth_facade = AuthFacade()
user_facade = UserFacade()

# Display all vacations sorted
@vacations_blueprint.route("/vacations") # Route
def list(): # View Function
    try:
        # Block a user who is not Logged in or Unregistered
        auth_facade.block_anonymous() 

        # Displaying vacations according to the sorting factor selected by the user: the default is Displaying vacations by  start date: 
        sort = request.args.get('sort')
        reverse = request.args.get('reverse') 
        all_vacations = vacations_facade.get_all_vacations_sorted(sort if sort != None else 'start_date', True if reverse != None else False)
        
        # Get all the "Like"s grouped by vacation_id
        likes= vacations_facade.get_all_likes()

        # Get a list of vacations (all the vacation_id) that the user marked "Like" 
        list_vacations_like = user_facade.get_list_vacations_like()

        #Check the user role (True = Admin. False = User):
        # If the user role ia Admin -> vacations_admin.html:
        if auth_facade.get_role_value(): 
            return render_template("vacations_admin.html", vacations = all_vacations, likes=likes, list_vacations_like=list_vacations_like,  active = "list")
        else:  
            #The user role is a User -> vacations_users.html :
            return render_template("vacations_users.html", vacations = all_vacations, likes=likes, list_vacations_like=list_vacations_like,  active = "list")
    
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message))# Send error to url query string


# Display single vacation:
@vacations_blueprint.route("/vacations/details/<int:vacation_id>") # <int:vacation_id> is the route parameter
def details(vacation_id):
    try:
        # Blocking a user who is not Logged in or Unregistered
        auth_facade.block_anonymous()

        # Get one vacation:
        one_vacation = vacations_facade.get_one_vacation(vacation_id)
        
        #Get the number of "Like"s for one vacation by the vacation_id
        likes_for_vacation = vacations_facade.get_likes_for_vacation(vacation_id)
        
        # Check if the user already check Like (=True) and or not (=False)
        is_like_by_current_user = user_facade.is_like_by_current_user(vacation_id)
        
        #Check the user role (True = Admin. False = User):
        # If the user role ia Admin -> details_admin.html:
        if auth_facade.get_role_value(): 
            return render_template("details_admin.html", vacation = one_vacation, likes_for_vacation=likes_for_vacation)
        else:  
            #The user role is a User -> details_users.html :
            return render_template("details_users.html", vacation = one_vacation, likes_for_vacation=likes_for_vacation, is_like_by_current_user=is_like_by_current_user)
    
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message))# Send error to url query string
    except ResourceNotFoundError as err:
        return render_template ("404.html", error = err.message)


# Return image file:
@vacations_blueprint.route("/vacations/images/<string:file_name>")
def get_image(file_name):
    image_path = ImageHandler.get_image_path(file_name)
    return send_file(image_path) # Returns a complete file (an image file with pixels of the image...)


# Adding new vacation:
@vacations_blueprint.route("/vacations/new", methods=["GET", "POST"])
def insert():
    try:
        # Block non-admin user
        auth_facade.block_non_admin()

        # If the request method is GET:
        if request.method == "GET": 
            # Get a list of countries for the user to select from:
            countries = vacations_facade.get_all_countries()
            return render_template("insert.html", countries=countries, form_data ={})

        # If the request method is POST:
        vacations_facade.add_vacation()
        return redirect (url_for ("vacations_view.list"))
    
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message)) # Send error to url query string      
    except ValidationError as err:
        # Pass the form data back to the template
        form_data = {
            "country_id": int(request.form.get("country_id")),
            "description": request.form.get("description"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "price": request.form.get("price"),
            "image": request.files["image"].filename #You can see the file_name due to the frontend validation
        }
        # Get a list of countries for the user to select from:
        countries = vacations_facade.get_all_countries()
        return render_template("insert.html", countries=countries, error=err.message, form_data=form_data) 

# Updating an existing vacation:
@vacations_blueprint.route("/vacations/edit/<int:vacation_id>", methods=["GET", "POST"])
def edit(vacation_id):
    try:
        # Block non-admin user
        auth_facade.block_non_admin()

        # If the request method is GET: 
        if request.method == "GET":
            one_vacation= vacations_facade.get_one_vacation(vacation_id) # Get all the vacation data/information
            countries = vacations_facade.get_all_countries() # Get a list of countries for the user to select from:
            return render_template("edit.html", vacation=one_vacation, countries= countries)
       
        # If the request method is POST:
        vacations_facade.update_vacation()
        # return redirect (url_for ("vacations_view.details", vacation_id=vacation_id))
        return redirect(url_for("vacations_view.list"))

    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message)) # Send error to url query string 
    except ResourceNotFoundError as err:
        return render_template("404.html", error = err.message) 
    except ValidationError as err:
        # Pass the form data back to the template
        form_data = {
            "country_id": request.form.get("country_id"),
            "description": request.form.get("description"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "price": request.form.get("price"),
            "file_name": request.form.get("image")  
        }
        one_vacation = vacations_facade.get_one_vacation(vacation_id) # Get all the vacation information
        countries = vacations_facade.get_all_countries() # Get a list of countries for the user to select from
        return render_template("edit.html", error=err.message, vacation=one_vacation, form_data=form_data, countries=countries)

# Delete existing vacation:
@vacations_blueprint.route("/vacations/delete/<int:vacation_id>")
def delete(vacation_id):
    try: 
        # Block non-admin user
        auth_facade.block_non_admin()
        vacations_facade.delete_vacation(vacation_id)
        return redirect(url_for("vacations_view.list"))
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message)) # Send error to url query string 

# Add like to a vacation:
@vacations_blueprint.route("/vacations/like/<int:vacation_id>") # <int:vacation_id> is the route parameter
def add_like(vacation_id): 
    try:
        # Blocking a user who is not Logged in or is an Admin
        auth_facade.block_anonymous()
        auth_facade.block_admin()

        #Getting user ID from the session:
        user = session.get("current_user") 
        user_id = user["user_id"]

        # Check if the user already marked "like" to this vacation before - block and raise error if needed 
        vacations_facade.block_duplicate_likes(user_id,vacation_id)

        vacations_facade.add_like(user_id, vacation_id)
        return redirect(url_for("vacations_view.list"))

    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message))# Redirect to login page with error message
    except ResourceNotFoundError as err:
        return render_template ("404.html", error = err.message)# Render 404 page with error message
    except ValidationError as err:
        flash(err.message, 'error') #display the validation error 
        return redirect(url_for("vacations_view.list"))# Redirect to vacations page with error message

   

# Delete like :
@vacations_blueprint.route("/vacations/unlike/<int:vacation_id>") # <int:vacation_id> is the route parameter
def delete_like(vacation_id):
    try:
        # Blocking a user who is not Logged in or is an Admin
        auth_facade.block_anonymous()
        auth_facade.block_admin()

        #Getting user ID from the session:
        user = session.get("current_user") 
        user_id = user["user_id"]

        vacations_facade.delete_like(user_id, vacation_id)
        return redirect(url_for("vacations_view.list"))

    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message))# Redirect to login page with error message
