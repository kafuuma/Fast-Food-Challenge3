from app.models.db_actions import UserDbQueries

class Users:
    """This class handles creation and storing users in a Datastructure"""

    def __init__(self, email, password,full_name="", contact="" ,user_role=""):
        self.full_name = full_name
        self.password = password
        self.email = email
        self.contact = contact
        self.user_role = user_role
        self.user_id = 0

    def signup(self):
        UserDbQueries().create_user(self)

    def login(self):
        user_data = UserDbQueries().fetch_user(self)
        if user_data:
            return self.convert_db_output_to_obj(user_data)
        return None
   
    def convert_db_output_to_obj(self, output):
        user = Users(
            output[0]["email"], output[0]["password"], output[0]["full_name"],
            output[0]["contact"],output[0]["user_role"]
        )
        user.user_id = output[0]["user_id"]
        return user