from flask import request
from flask_restful import Resource
from app.models.validate import VerifyMenu, VerifyToken
from app.models.orders import Orders
from app.models.db_actions import OrderDbQueries

class PlaceOrders(Resource):
    """
    This class inherits from the resource class
    it implements an end point to place orders
    """
    def post(self):
        user_request = request.get_json()
        print(user_request)
        if user_request:
            auth_token = request.headers["Authentication"]
            user_info = VerifyToken.validate(auth_token)
            menu_id = user_request.get("menu_id")
            if user_info:
                if not VerifyMenu.check_menu_id(menu_id):
                    return {"message":"menu_id must be integer"},400
                try:
                    Orders(user_info["email"],menu_id).create_order()
                    if OrderDbQueries().fetch_order(user_info["email"], menu_id):
                        return{"message":"successfuly placed food order"},200
                    return{"message":"order not successful"},404
                except:
                    return{"message":"menu doesnt exist"},404
            return{"message":"not authenticated"},401
        return {"message":"empty fields"},400
