from logic.auth_logic import AuthLogic
from flask import request, session
from models.user_model import UserModel
from models.credentials_model import CredentialsModel
from models.role_model import RoleModel
from models.client_errors import ValidationError, AuthError
from utils.cyber import Cyber

class AuthFacade: 

    #Ctor
    def __init__(self):
        self.logic=AuthLogic()

    # Register a new user:
    def register(self):
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        user = UserModel (None, first_name, last_name, email, password, RoleModel.User.value)
        error = user.validate_insert()
        if error: raise ValidationError(error, user)
        if self.logic.is_email_taken(email): raise ValidationError ("Email already exists.", user)    
        user.password = Cyber.hash(user.password)
        self.logic.add_user(user)
        user = self.logic.get_user(user.email, user.password) # Get the dictionary user from database
        del user["password"] # Remove passwords from session.
        session["current_user"] = user # Save the user inside the session dictionary.

    #Login 
    def login(self):
        email=request.form.get("email")
        password=request.form.get("password")
        credentials = CredentialsModel(email, password)
        error = credentials.validate()
        if error: raise ValidationError (error,credentials)
        hashed_password = Cyber.hash(credentials.password)
        user = self.logic.get_user(credentials.email, hashed_password)
        if not user: raise AuthError("Incorrect email or password.", credentials)
        del user["password"] # Remove passwords from session.
        session ["current_user"] = user #save the user inside the session dictionary. 
    
    #Logout
    def logout(self):
        session.clear()

    #Get the role value (to check if he is Admin = True or User = False) for the HTML:
    def get_role_value (self):
        user = session.get("current_user")
        if user["role_id"] == RoleModel.Admin.value:
            return True
        else:
            return False

    # Block non logged-in users: 
    def block_anonymous(self):
        user = session.get("current_user")
        if not user: raise AuthError ("You are not logged-in.")

    # Block non admin users: 
    def block_non_admin(self): 
        user = session.get("current_user")
        if not user: raise AuthError ("You are not  logged-in.") #Check if user is logged-in
        if user["role_id"] != RoleModel.Admin.value: raise AuthError ("You are not authorized.") #Check if user is authorized (Admin)

    # Block admin users: 
    def block_admin(self): 
        user = session.get("current_user")
        if not user: raise AuthError ("You are not  logged-in.") #Check if user is logged-in
        if user["role_id"] != RoleModel.User.value: raise AuthError ("You are not authorized.") #Check if user is authorized (User)


    #Close connection: 
    def close(self):
        self.logic.close()

