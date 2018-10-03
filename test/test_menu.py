
import json
from app.models.db_actions import UserDbQueries
from app.models.menu import Menu
from test.main_test import BaseTest

class TestMenu(BaseTest):

    def test_menu_object_creation(self):
        menu = Menu()
        self.assertIsInstance(menu, Menu)

    def test_menu_item_creation(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        response = self.test_client.post(
                   "/api/v1/menu",
                   content_type="application/json",
                data=json.dumps({
                    "menu_name":"chicken bucket",
                    "description": "4 pieces served with juice",
                    "menu_price": 50000
                }),

                   headers={
                       "Authentication": auth_token,
                       
                   }
            )

        print(json.loads(response.data), "strjjghjkl")
        self.assertEqual(response.status_code,201)
        
  