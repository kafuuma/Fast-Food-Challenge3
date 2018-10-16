
import json
from app.models.db_actions import UserDbQueries
from app.models.users import Users
from test.main_test import BaseTest
class TestFastFood(BaseTest):

  
    def test_user_object_creation(self):
        user = Users("ark@gmail.com",'topsecret')
        self.assertIsInstance(user, Users)

    def test_database_object_creation(self):
        db = UserDbQueries()
        self.assertIsInstance(db, UserDbQueries)

    def test_user_signup(self):
        response = self.post_signup_data(
            "henry henry", "ark@gmail.com","topsecret","topsecret","07777777777","user"   
        )
        self.assertEqual(response.status_code,201)
        self.assertEqual(json.loads(response.data.decode()),{"message":"signup successfull"})
       
    def test_signup_already_existing_user(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","topsecret","topsecret","07777777777","user"   
           )
        response = self.post_signup_data(
            "henry henry", "ark@gmail.com","topsecret","topsecret","07777777777","user"   
         )
        self.assertEqual(response.status_code,409)
        self.assertEqual(json.loads(response.data.decode()),{"message":"user exists"})

    def test_signup_unmatching_passwords(self):
        response = self.post_signup_data(
            "henry henry", "ark@gmail.com","topsecret","toptopsecret","07777777777","user"   
           )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data.decode()),{"message": "Passwords do not match"})
    
    def test_signup_empty_fields(self):
        response = self.test_client.post(
                "/api/v1/auth/signup",
                content_type="application/json",
                data= json.dumps({})
            )
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data.decode()),{"message": "Fields Empty"})
        
    def test_user_login(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","topsecret","topsecret","07777777777","user"
            )
        response =self.post_user_login_data("ark@gmail.com", "topsecret")
        print(json.loads(response.data.decode()))
        user_info = self.decode_token(json.loads(response.data.decode()))
        self.assertEqual(response.status_code,200)
        self.assertEqual(user_info["email"], "ark@gmail.com")
        self.assertEqual(user_info["user_role"], "user")

    def test_user_login_invalid_pasword(self):
        self.post_signup_data(
            "henry henry", "ark@gmail.com","topsecret","topsecret","07777777777","user"
            )
        response =self.post_user_login_data("ark@gmail.com", "toptopsecret")
        self.assertEqual(response.status_code,401)
        self.assertEqual(json.loads(response.data.decode()),{"message":"wrong password"})

    def test_login_non_existing_user(self):
        response =self.post_user_login_data("ark@gmail.com", "toptopsecret")
        self.assertEqual(response.status_code,400)
        self.assertEqual(json.loads(response.data.decode()),{"message":"User doesnt exist"})

    def test_log_in_empty_fields(self):
        response = self.test_client.post(
                   "/api/v1/auth/login",
                content_type="application/json",
                data= json.dumps({})
            )
        self.assertEqual(response.status_code,409)
        self.assertEqual(json.loads(response.data.decode()), {"message":"empty fields"})
  
 



        

        

