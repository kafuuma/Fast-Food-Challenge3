import re
from jwt import decode
from app import app


class VerifyToken:
    """
    This class has a static method that decodes tokens
    """
    @staticmethod
    def validate(token):
        try:
            user_info = decode(token, app.config["SECRET_KEY"])
            return user_info
            
        except:
            return None
    

class VerifyUsers:

    """This class verifies user data and checks it for validity"""

    def __init__(self,password, email, full_name="",  contact="", user_role=""):
        self.full_name = full_name
        self.password = password
        self.email = email
        self.contact = contact
        self.user_role = user_role

    def check_empty_login(self):
        if len(self.email.strip(" ")) == 0 or len(self.password.strip(" ")) ==0:
            return False
        return True

    def check_if_empty(self):
        """This checks if field is empty"""
        if len(self.full_name.strip(" ")) == 0 or len(self.password.strip(" ")) ==0 or len(self.email.strip(" ")) == 0\
            or len(self.contact.strip(" ")) ==0 or len(self.user_role.strip(" ")) == 0:
            return False
        return True

    def check_username(self):
        """This checks if useranme is of length and and not containg special chrs"""
        if re.match(r"^[a-zA-Z\s]{8,20}$", self.full_name):
            return True
        return False

    def check_password(self):
        """This checks password length"""
        if len(self.password) >= 8:
            return True
        return False

    def check_email(self):
        """This checks email address"""
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]{2,3}$", self.email):
            return True
        return False


class VerifyMenu:

    def __init__(self, menu_name, description, menu_price):
        self.menu_name = menu_name
        self.description = description
        self.menu_price = menu_price

    def check_if_empty(self):
        """This checks if field is empty"""
        if len(self.menu_name.strip(" ")) == 0 or len(self.description.strip(" ")) ==0:
            return False
        return True

    def check_menu_name(self):
        if self.menu_name.isalnum():
            return True
        return False
    
    def check_menu_price(self):
        if isinstance(float(self.menu_price),float) or isinstance(self.menu_price, float):
            return True
        return False
   
    @staticmethod
    def check_menu_id(menu_id):
        if isinstance(menu_id, int):
            return True
        return False


class VerifyOrders:
        def __init__(self, order_id,status):
            self.order_id = order_id
            self.status = status

        def check_order(self):
            if len(self.status.strip(" ")) != 0 and isinstance(self.order_id,int):
                return True
            return False
