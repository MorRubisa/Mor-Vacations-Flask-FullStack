from logic.vacations_logic import VacationsLogic
from logic.user_logic import UserLogic
from operator import attrgetter
from flask import request #Request object arrived from the frontend
from flask import session #Session for the like list
from models.vacation_model import VacationModel
from models.client_errors import ResourceNotFoundError, ValidationError


class VacationsFacade:

    # ctor - create the logic:
    def __init__(self):
        self.vacations_logic = VacationsLogic()
        self.user_logic = UserLogic()

    # Get all vacations (not sorted): 
    def get_all_vacations(self):
        return self.vacations_logic.get_all_vacations()
    
    # Get all the vacations sorted by a sorting factor (with an option for a reversed list, default is False):
    def get_all_vacations_sorted(self, sorting_factor = "start_date", reverse=False):

        # Check if "sorting_factor" is in fact a Vacation Model attribute:
        if not sorting_factor.lower() in ("vacation_id", "country_id", "description", "start_date", "end_date", "price", "file_name", "country_name"):
            raise ValueError(
                "The sorting factor sent is not a vacation attribute.")

        # Get all vacations:
        vacations_list = self.vacations_logic.get_all_vacations()

        # Sort the vacations list by the sorting factor sent (using the "operator" module to convert the string to a Vacation Model attribute):
        sorted_vacations_list = sorted(vacations_list, key=lambda x: x[sorting_factor.lower()], reverse=reverse)
        
        return sorted_vacations_list

    # Get one vacation:
    def get_one_vacation (self, vacation_id):
        vacation = self.vacations_logic.get_one_vacation(vacation_id)
        if not vacation: raise ResourceNotFoundError(vacation_id)
        return vacation

    #Get all countries
    def get_all_countries (self):
        return self.vacations_logic.get_all_countries()

    #Add new vacation
    def add_vacation(self):
        country_id = request.form.get("country_id") 
        description = request.form.get("description") 
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date") 
        price = request.form.get("price") 
        file_name = request.files["image"] 
        
        # Get a collection of countries IDs:
        countries_ids = self.vacations_logic.get_all_countries_ids()

        # Creating a vacation: 
        vacation = VacationModel (None, country_id, description, start_date, end_date, price, file_name)
        
        # Validation tests: 
        error = vacation.validate_insert(countries_ids)
        if error: raise ValidationError(error, vacation)

        self.vacations_logic.add_vacation(vacation)

    #Update an existing vacation
    def update_vacation(self):
        vacation_id= request.form.get ("vacation_id")
        country_id = request.form.get("country_id") 
        description = request.form.get("description") 
        start_date = request.form.get("start_date") 
        end_date = request.form.get("end_date") 
        price = request.form.get("price") 
        file_name = request.files["image"] 
        vacation = VacationModel (vacation_id, country_id, description, start_date, end_date, price, file_name)
 
        # Get a collection of countries IDs:
        countries_ids = self.vacations_logic.get_all_countries_ids()

        error = vacation.validate_update(countries_ids)

        if error: raise ValidationError(error, vacation)
        self.vacations_logic.update_vacation(vacation)
    

    # Delete existing product:
    def delete_vacation(self, vacation_id):
        self.vacations_logic.delete_vacation(vacation_id)


    #Get a collection of all "Like"s grouped by vacation_id and the number of likes
    def get_all_likes (self):
        # Get a table of all "Like"s grouped by vacation_id
        likes_collection =  self.vacations_logic.get_all_likes()

        # Turn the table in a dictionary 
        likes_dictionary = {}
        for like in likes_collection: 
            vacation_id = like ["vacation_id"]
            likes = like ["likes"] 
            likes_dictionary[vacation_id]=likes
        return likes_dictionary

    #Get the number of likes for a one vacation by the vacation_id
    def get_likes_for_vacation(self, vacation_id):
        return self.vacations_logic.get_likes_for_vacation(vacation_id)

    #Add like by user (with the user_id) to a vacation (by vacation_id)
    def add_like (self, user_id, vacation_id):

        # Check if the vacation exist in the database:
        check_vacation = self.vacations_logic.get_one_vacation(vacation_id)
        if check_vacation is None:
            raise ResourceNotFoundError(vacation_id)   

        # After checking that both the user and vacation exist -> add the Like:
        self.user_logic.add_like(user_id, vacation_id)

    # Check if the user already marked "like" to this vacation before:
    def block_duplicate_likes (self, user_id, vacation_id):
        if self.user_logic.check_like(user_id, vacation_id):
            raise ValidationError("You can't check LIKE again! Check LIKE only once per vacation", None) #None is the "model" argument since there is no specific model instance

    # Delete like:
    def delete_like(self, user_id, vacation_id):

        # Don't need to Check if the user and the vacation exist in the database therefor:
        self.user_logic.delete_like(user_id, vacation_id)

    # Close connection:
    def close(self):
        self.vacations_logic.close()
        self.user_logic.close()

