import re
from app.models.users import Users
from app.models.menu import Menu
from app.models.orders import Orders
from jwt import decode
from app import app


class VerifyToken:
    @staticmethod
    def validate(token):
        try:
            user_info = decode(token, app.config["SECRET_KEY"])
            return user_info
            
        except:
            return None
    
class VerifyUsers(Users):
    pass


class VerifyMenu(Menu):
    pass

class VerifyOrders(Orders):
    pass