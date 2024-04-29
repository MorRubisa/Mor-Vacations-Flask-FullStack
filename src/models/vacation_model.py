from datetime import *

# Vacation Model:
class VacationModel:

    # Ctor:
    def __init__(self, vacation_id, country_id, description, start_date, end_date, price, file_name):
        self.vacation_id = vacation_id
        self.country_id = country_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.file_name = file_name #image file

    # Validating a new vacation insert:
    def validate_insert (self, countries_ids): 
        # Check if all arguments were assigned values:
        if not self.country_id: return "Missing Country"
        if not self.description: return "Missing Description"
        if not self.start_date: return "Missing Start Date"
        if not self.end_date: return "Missing End Date"
        if not self.price: return "Missing Price"
        if not self.file_name: return "Missing Image"
        
        # Check if the selected country exists in the countries table (by checking the country ID ): 
        if int(self.country_id) not in list(map(lambda x: x["country_id"], countries_ids)):
            return "Invalid Country"

        #Check if the length of the description is between 2-1000 chars
        if len(self.description) <2 or len(self.description)>1000: return "Description length must be 2-1000 chars."

        # Check if price is between 0 to 10,000:
        if float(self.price) <0 or float(self.price)>10000: return "The price must be between $0 and $10,000."


        # Check the current date and convert the date strings into date format by using the "datetime" module:
        current_date = datetime.now().date()
        formatted_start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        formatted_end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()

        # Check if the given starting date is not in the past:
        if current_date > formatted_start_date:
            return "The start date can't be in the past"

        # Check that the start date is before the end date:
        if formatted_start_date > formatted_end_date:
            return "The end date of the vacation can't be before the start date"
        
        #If there is no error  - return None 
        return None # No error.

    # Validating an existing vacation update:
    def validate_update (self, countries_ids): 
        # Check if all arguments were assigned values:
        print(self)
        if not self.vacation_id: return "Missing vacation ID"
        if not self.country_id: return "Missing Country"
        if not self.description: return "Missing Description"
        if not self.start_date: return "Missing Start Date"
        if not self.end_date: return "Missing End Date"
        if not self.price: return "Missing Price"

        #Check if the length of the description is between 2-1000 chars
        if len(self.description) <2 or len(self.description)>1000: return "Description length must be 2-1000 chars."

        # Check if price is between 0 to 10,000:
        if float(self.price) <0 or float(self.price)>10000: return "The price must be between $0 and $10,000."

        # Check if the selected country exists in the countries table (by checking the country ID ): 
        if int(self.country_id) not in list(map(lambda x: x["country_id"], countries_ids)):
            return "Invalid Country"

        # Convert the date strings into date format by using the "datetime" module:
        formatted_start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        formatted_end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()

        # Check that the start date is before the end date:
        if formatted_start_date > formatted_end_date:
            return "The end date of the vacation can't be before the start date"
        
        #If there is no error  - return None 
        return None # No error.