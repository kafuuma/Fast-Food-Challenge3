
import unittest
import json
from run import app
from app.models.db_actions import UserDbQueries


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


    def test_creation_of_user_table(self):
        try:
            self.db.create_table()
        except:
            response = {"response":"table_already exists"}
        self.assertEquals(response, {"response":"table_already exists"})
