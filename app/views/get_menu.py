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
        auth_token = request.headers["Authentication"]
        user_info = VerifyToken.validate(auth_token)
        if user_info:
            response = MenuDbQueries().fetch_all_menu()
            if response:
                return{"menu": response,
                       "message":"successfuly fetched all menu"},200
            return {"message":"menu_doesn't exist"},404
        return{"message":"Not Authenticated"},401
    
