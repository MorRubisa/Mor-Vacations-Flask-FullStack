from utils.dal import DAL
from utils.image_handler import ImageHandler

class VacationsLogic():

    def __init__ (self):
        self.dal = DAL()

    # Return all vacations:
    def get_all_vacations(self):
        sql = "SELECT * FROM vacations JOIN countries ON vacations.country_id=countries.country_id"
        result = self.dal.get_table(sql)
        return result 
    
    # Return one vacation by vacation ID:
    def get_one_vacation(self, vacation_id):
        sql = """
            SELECT vacations.*, countries.country_name 
            FROM vacations 
            JOIN countries ON vacations.country_id = countries.country_id 
            WHERE vacation_id = %s
            """
        result = self.dal.get_scalar(sql, (vacation_id,))
        if not result:
            return None  # If the dictionary is empty (meaning vacation ID does not exist) return None.
        return result

    # Return one country by country ID:
    def get_country(self, country_id):
        sql = "SELECT * FROM countries WHERE country_id = %s"
        result = self.dal.get_scalar(sql, (country_id, ))
        return result 

    # Return all countries in the DataBase:
    def get_all_countries(self):
        sql = "SELECT * FROM countries"
        result = self.dal.get_table(sql)
        return result 

    # Return all countries' IDs:
    def get_all_countries_ids(self):
        sql = "SELECT country_id FROM countries"
        result = self.dal.get_table(sql)
        return result

    # Return all countries' names:
    def get_all_countries_names(self):
        sql = "SELECT country_name FROM countries"
        result = self.dal.get_table(sql)
        return result

    # Return all likes grouped by vacation_id:
    def get_all_likes(self):
        sql = "SELECT vacation_id, COUNT(user_id) AS likes FROM likes GROUP BY vacation_id"
        result = self.dal.get_table(sql)
        return result 

    #Get the number of LIKES for a single vacation (by the vacation_id)    
    def get_likes_for_vacation(self, vacation_id):
        sql = "SELECT COUNT(*) AS like_count FROM likes WHERE vacation_id = %s"
        params = (vacation_id,)
        likes_count = self.dal.get_scalar(sql, params)
        return likes_count["like_count"]

    # Add a new vacation:
    def add_vacation(self, vacation):
        file_name = ImageHandler.save_image(vacation.file_name)
        sql = "INSERT INTO vacations (country_id, description, start_date, end_date, price, file_name) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (vacation.country_id, vacation.description, vacation.start_date, vacation.end_date, vacation.price, file_name)
        self.dal.insert(sql, params)

    # Update an existing vacation: 
    def update_vacation(self, vacation):
        old_image_name = self.__get_old_image_name(vacation.vacation_id)
        image_name = ImageHandler.update_image(old_image_name, vacation.file_name)
        sql = "UPDATE vacations SET country_id=%s, description=%s, start_date=%s, end_date=%s, price=%s, file_name=%s  WHERE vacation_id=%s"
        self.dal.update(sql, (vacation.country_id, vacation.description, vacation.start_date, vacation.end_date, vacation.price, image_name, vacation.vacation_id))

    #Get the old image name for later use:
    def __get_old_image_name(self, vacation_id):
        sql = "SELECT file_name FROM vacations WHERE vacation_id=%s"
        result = self.dal.get_scalar(sql, (vacation_id, ))
        if result is not None:
            return result["file_name"]
        else: 
            return None

    # Delete existing vacation:
    def delete_vacation(self, vacation_id):
        image_name = self.__get_old_image_name(vacation_id)
        ImageHandler.delete_image(image_name)
        sql = "DELETE FROM vacations WHERE vacation_id=%s"
        self.dal.delete(sql, (vacation_id, ))
    
    # Close connection:
    def close(self):
        self.dal.close()
    
