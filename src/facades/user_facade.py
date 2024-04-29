from logic.user_logic import UserLogic
from flask import session #Session for the like list
from models.client_errors import ResourceNotFoundError, ValidationError


class UserFacade:

    # ctor - create the logic:
    def __init__(self):
        self.user_logic = UserLogic()

    # Check if the user already "Like" this vacation (by vacation_id)
    def is_like_by_current_user(self, vacation_id):
        # Getting the user ID from the session:
        current_user = session.get("current_user") 
        current_user_id = current_user["user_id"]

        # Return True if the user already check "Like" and False if not
        return self.user_logic.check_like(current_user_id,vacation_id)

    # Return a LIST of all the vacations_id that the current user check "LIKE":
    def get_list_vacations_like(self):
        # Getting the user ID from the session:
        current_user = session.get("current_user") 
        current_user_id = current_user["user_id"]
        return self.user_logic.get_list_vacations_like(current_user_id) 
  
    # Close connection:
    def close(self):
        self.user_logic.close()

