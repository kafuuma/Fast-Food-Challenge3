
import unittest
import json
from run import app
from app.models.db_actions import MenuDbQueries,UserDbQueries,OrderDbQueries
from app.models.validate import VerifyToken
from app.models.menu import Menu
from app.models.users import Users
from app.views import login, signup
from jwt import decode

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.test_client = self.app.test_client()
        self.dbmenu = MenuDbQueries()
        self.dbuser = UserDbQueries()
        self.dborders= OrderDbQueries()
        self.dbuser.create_table()
        self.dbmenu.create_table()
        self.dborders.create_table()

    def tearDown(self):
        self.dbuser.drop_table()
        self.dborders.drop_table()
        self.dbmenu.drop_table()
       
      
    
    def post_signup_data(self, user_name, email, password, confirm_password,contact, user_role):
            response = self.test_client.post(
                    "/api/v1/auth/signup",
                    content_type="application/json",
                    data= json.dumps({
                        "full_name":user_name,
                        "email":email,
                        "password":password,
                        "contact":contact,
                        "confirm_password":confirm_password,
                        "user_role":user_role
                        }
                    )
                )
            return response
    
    def post_user_login_data(self,email, password):
        response = self.test_client.post(
                   "/api/v1/auth/login",
                content_type="application/json",
                data= json.dumps({
                    "email":email,
                    "password":password,
                    }
                )
            )
        return response

    def decode_token(self, token):
        user_info = decode(token["Authentication"], app.config["SECRET_KEY"])
        return user_info
