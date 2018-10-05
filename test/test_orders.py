import json
from app.models.db_actions import UserDbQueries
from app.models.orders import Orders
from test.main_test import BaseTest

class TestOrders(BaseTest):
    
   
    def generate_admin_token(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        return auth_token

    def test_order_object_creation(self):
        order = Orders()
        self.assertIsInstance(order, Orders)

    def test_place_order(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        self.post_menu_data(auth_token)
        response = self.post_order_data(1,auth_token)
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.data.decode()),{"message":"successfuly placed food order"})
    
    def test_place_non_existing_menu_order(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        self.post_menu_data(auth_token)
        response = self.post_order_data(6,auth_token)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json.loads(response.data.decode()),{"message":"menu doesnt exist"})

    def test_place_order_non_authenticate_user(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        self.post_menu_data(auth_token)
        response = self.post_order_data(6,auth_token+"sdfghjgfdfgh")
        self.assertEqual(response.status_code,401)
        self.assertEqual(json.loads(response.data.decode()),{"message":"not authenticated"})

    def test_place_with_empty_field(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","admin"
            )
        user_info =self.post_user_login_data("ark@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        self.post_menu_data(auth_token)
        self.post_signup_data(
            "henry henry", "arrk@gmail.com","secret","secret","07777777777","user"
            )
        user_info =self.post_user_login_data("arrk@gmail.com", "secret")
        token_info = json.loads(user_info.data.decode())
        auth_token = token_info["Authentication"]
        response = self.test_client.post(
                    "/api/v1/users/orders",
                    content_type="application/json",
                data=json.dumps({}),
                    headers={
                        "Authentication":auth_token   
                    }
            )
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data.decode()),{"message":"empty fields"})
        
    # def test_get_order_history(self):
    #     self.post_menu_data(self.admin_token)
    #     self.post_order_data(1,self.user_token)
    #     self.post_order_data(1,self.user_token)
    #     response = self.get_order_history_data(self.user_token)
    #     self.assertEqual(response.status_code,200)
        
    # def test_fetch_no_orders(self):
    #     response = self.get_order_history_data(self.user_token)
    #     self.assertEqual(response.status_code,404)
    #     self.assertEqual(json.loads(response.data.decode()),{"message":"no orders for you"})
    
    # def test_fetch_order_history_non_authenticated_user(self):
    #     self.post_menu_data(self.admin_token)
    #     self.post_order_data(1,self.user_token)
    #     self.post_order_data(1,self.user_token)
    #     response = self.get_order_history_data(self.user_token+" ")
    #     self.assertEqual(response.status_code,401)
    #     self.assertEqual(json.loads(response.data.decode()),{"message":"not authenticated"})
      

