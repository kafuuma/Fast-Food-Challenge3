from flask import request
from flask_restful import Resource
from app.models.validate import VerifyMenu, VerifyToken
from app.models.menu import Menu
from app.models.db_actions import MenuDbQueries

class GetMenu(Resource):
    """
    This class implements from the resource classs
    It iplements an end point to fetch menu items
    """
    def get(self):
        response = MenuDbQueries().fetch_all_menu()
        if response:
            return{"menu": response,
                    "message":"successfuly fetched all menu"},200
        return {"message":"menu_doesn't exist"},404
    
