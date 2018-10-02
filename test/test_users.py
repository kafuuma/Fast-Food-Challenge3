
import unittest
import json
from run import app
from app.models.db_actions import UserDbQueries
from app.models.validate import VerifyToken
from app.models.users import Users
from jwt import decode


class TestFastFood(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.test_client = self.app.test_client()
        # self.app_context = app.app_context()
        # self.app_context.push()
        self.db = UserDbQueries()
        self.db.create_table()
            
    def tearDown(self):
       self.db.drop_table()
    
    #write tests for user signup
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

    def test_user_object_creation(self):
        user = Users("ark@gmail.com",'secret')
        self.assertIsInstance(user, Users)

    def test_database_object_creation(self):
        self.assertIsInstance(self.db, UserDbQueries)

    def test_user_signup(self):
        response = self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","user"   
        )
        self.assertEqual(response.status_code,201)
        self.assertEqual(json.loads(response.data.decode()),{"response":"signup successfull"})
       
    def test_signup_already_existing_user(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","user"   
           )
        response = self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","user"   
         )
        self.assertEqual(response.status_code,409)
        self.assertEqual(json.loads(response.data.decode()),{"response":"user exists"})

    def test_signup_unmatching_passwords(self):
        response = self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","topsecret","07777777777","user"   
           )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data.decode()),{"response": "Passwords do not match"})
    
    def test_signup_empty_fields(self):
        response = self.test_client.post(
                "/api/v1/auth/signup",
                content_type="application/json",
                data= json.dumps({})
            )
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data.decode()),{"response": "Fields Empty"})
        
    #write tests for user slogin

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

 
    def test_user_login(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","user"
            )
        response =self.post_user_login_data("ark@gmail.com", "secret")
        user_info = self.decode_token(json.loads(response.data.decode()))
        print(user_info)
        self.assertEqual(response.status_code,200)
        self.assertEqual(user_info["email"], "ark@gmail.com")
        # self.assertEqual(user_info["user_role"], "user")

    def test_user_login_invalid_pasword(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","secret","secret","07777777777","user"
            )
        response =self.post_user_login_data("ark@gmail.com", "topsecret")
        self.assertEqual(response.status_code,401)
        self.assertEqual(json.loads(response.data.decode()),{"response":"wrong password"})

    def test_login_non_existing_user(self):
        response =self.post_user_login_data("ark@gmail.com", "topsecret")
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data.decode()),{"response":"User doesnt exist"})

    def test_log_in_empty_fields(self):
        response = self.test_client.post(
                   "/api/v1/auth/login",
                content_type="application/json",
                data= json.dumps({})
            )
        self.assertEqual(response.status_code,409)
        self.assertEqual(json.loads(response.data.decode()), {"response":"empty fields"})



        

        

