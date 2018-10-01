
import unittest
import json
from run import app
from app.models.db_actions import UserDbQueries
from app.models.users import Users


class TestFastFood(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.test_client = self.app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
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

    def post_user_login_data(self):
        response = self.test_client.post(
            
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
        
    