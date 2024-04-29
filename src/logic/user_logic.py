from utils.dal import DAL

class UserLogic():

    def __init__(self):
        self.dal= DAL()

    # Get a user by user ID:
    def get_one_user_by_id(self, user_id):
        sql = "SELECT * FROM users WHERE user_id = %s"
        user = self.dal.get_scalar(sql, (user_id, ))
        if user is None: return None # In case there is no user with this ID return None.
        return user

    # Check if the "Like" already exists, return True if it is, and False if not:
    def check_like(self, user_id, vacation_id):
        sql = "SELECT * FROM likes WHERE user_id = %s AND vacation_id = %s"
        params = (user_id, vacation_id)
        result = self.dal.get_scalar(sql, params)
        if result is None: return False
        return True

    # Return a LIST of all the vacations_id that the current user check "LIKE":
    def get_list_vacations_like(self, user_id):
        sql = "SELECT * FROM likes WHERE user_id = %s"
        params = (user_id, )
        like_table = self.dal.get_table(sql, params)

        # Turn the table to a list
        like_list = []
        for like in like_table: 
            vacation_id_liked = like["vacation_id"]
            like_list.append(vacation_id_liked)
        return like_list

    # User adding a like to a vacation:
    def add_like(self, user_id, vacation_id):
        sql = "INSERT INTO likes (user_id, vacation_id) VALUES (%s, %s)"
        params = (user_id, vacation_id)
        self.dal.insert(sql, params)
        
    # User removing a like from a vacation:
    def delete_like(self, user_id, vacation_id):
        sql = "DELETE FROM likes WHERE user_id = %s AND vacation_id = %s"
        params = (user_id, vacation_id)
        rows_affected_count = self.dal.delete(sql, params)
        return rows_affected_count


    # Close connection:
    def close(self):
        self.dal.close()
    

    