
import json
from app.models.db_actions import UserDbQueries
from app.models.menu import Menu
from test.main_test import BaseTest

class TestMenu(BaseTest):

    def test_menu_object_creation(self):
        menu = Menu()
        self.assertIsInstance(menu, Menu)

    def test_add_menu_item(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        print(auth_token)
        response = self.post_menu_data(auth_token)
        self.assertEqual(response.status_code,201)
        self.assertEqual(json.loads(response.data.decode()),{"message":"menu successfuly created"})
    
    def test_non_admin_user_menu_add_menu(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","user"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        response = self.post_menu_data(auth_token)
        self.assertEqual(response.status_code,401)
        self.assertEqual(json.loads(response.data.decode()),{"message":"Only admins create menu items"})
       
    def test_add_existing_menu_item(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        print(auth_token)
        self.post_menu_data(auth_token)
        response = self.post_menu_data(auth_token)
        self.assertEqual(response.status_code,409)
        self.assertEqual(json.loads(response.data.decode()),{"message":"menu_exists"})
    
    def test_add_menu_non_logged_in_user(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        auth_token = "@@#$%^&*()_!@#$%^&*()_+!@#$%^&*()_!@#$%^&*()_!@#$%^&*()_+!@#$%^&*()_!@#$"
        response = self.post_menu_data(auth_token)
        self.assertEqual(response.status_code,401)
        self.assertEqual(json.loads(response.data.decode()),{"message":"Not Authenticated"})
  
    def test_fetch_menu_admin_user(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        self.post_menu_data(auth_token)
        response = self.test_client.get(
                   "/api/v1/menu",
                   content_type="application/json",
                   headers={
                       "Authentication": auth_token    
                   }
            )
        self.assertEqual(response.status_code,200)
    
    def test_fetch_all_menu_normal_user(self):
        
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        self.post_signup_data(
            "henry henry", "henry@gmail.com","secret","secret","07777777777","user"
            )
        admin_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(admin_info.data.decode())
        auth_token = token_info["Authentication"]
        self.post_menu_data(auth_token)
        self.post_menu_data(auth_token)
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_infou = json.loads(user_info.data.decode())
        auth_tokenu = token_infou["Authentication"]
        response = self.test_client.get(
                   "/api/v1/menu",
                   content_type="application/json",
                   headers={
                       "Authentication": auth_tokenu    
                   }
            )
        self.assertEqual(response.status_code,200)
    
    def test_fetch_empty_orders(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        response = self.test_client.get(
                   "/api/v1/menu",
                   content_type="application/json",
                   headers={
                       "Authentication": auth_token    
                   }
            )
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data.decode()),{"message":"menu_doesn't exist"})
    
    
