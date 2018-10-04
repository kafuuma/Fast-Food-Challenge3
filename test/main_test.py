
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

    def post_menu_data(self, auth_token):
        response = self.test_client.post(
                   "/api/v1/menu",
                   content_type="application/json",
                data=json.dumps({
                    "menu_name":"chicken bucket",
                    "description": "4 pieces served with juice",
                    "menu_price": 50000
                }),

                   headers={
                       "Authentication": auth_token
                       
                   }
            )
        return response

    def post_order_data(self, menu_id, user_token):
        response = self.test_client.post(
                    "/api/v1/users/orders",
                    content_type="application/json",
                data=json.dumps({
                    "menu_id": menu_id
                }),
                    headers={
                        "Authentication":user_token    
                    }
            )
        return response

    
    def get_order_history_data(self, user_token):
        response = self.test_client.get(
                "/api/v1/users/orders",

                content_type="application/json",
                  
                headers={
                     "Authentication":user_token    
                    }
           )
        return response


    def token(self):
        self.post_signup_data(
           "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        return auth_token


        

    user_token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6InBia2RmMjpzaGEyNTY6NTAwMDAkaE5FNjV5Z1gkZDE3ZWRhNzYyZmVlM2Q3NGY5OWQ1YzU1ODk5MWUzMzNiOTFiYTVjYTI1Y2NlMGRkMzUxYjk2ZWU1N2E0NTJiMiIsImVtYWlsIjoiYXJrQGdtYWlsLmNvbSIsInVzZXJfcm9sZSI6ImFkbWluIn0.qt_xhXaEj59a2A2QFkkeFaubbeUsrCAhGt5CsB5MhkU"
        
    

    admin_token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6InBia2RmMjpzaGEyNTY6NTAwMDAkcVV2TllYNzgkYzc5OTJlNWRlYjY1YzY2MzAwOTcwYzdiZWU0YmNiNThjYzcwOGU3ZjExMDFkNjE0M2QyZWRmMjE5ZTIzZmZjMSIsImVtYWlsIjoiYXJrQGdtYWlsLmNvbSIsInVzZXJfcm9sZSI6ImFkbWluIn0.ULGqtqbogB4l8Ry27PXoG7Sl4oKDEoM5PsbAQ_PW6vY"
        
        
      
    

        