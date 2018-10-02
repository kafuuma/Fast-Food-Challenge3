import re
from app.models.users import Users
from jwt import decode
from app import app


class VerifyToken:
    @staticmethod
    def validate(token):
        print(app.config["SECRET_KEY"])
        # try:
        #     user_info = decode(token, app.config["SECRET_KEY"])
        #     return user_info
            
        # except:
        #     return None
        user_info = decode(token, app.config["SECRET_KEY"])
        return user_info

class VerifyUsers(Users):
    pass
