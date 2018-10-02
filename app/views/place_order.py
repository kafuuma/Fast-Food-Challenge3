from flask import request
from flask_restful import Resource
from app.models.validate import VerifyOrders, VerifyToken
from app.models.orders import Orders
from app.models.db_actions import OrderDbQueries

class PlaceOrders(Resource):
    def post(self):
        user_request = request.get_json()
        if user_request:
            auth_token = request.headers["Authentication"]
            user_info = VerifyToken.validate(auth_token)
            menu_id = user_request.get("menu_id")
            if user_info:
                try:
                    Orders(user_info["email"],menu_id).create_order()
                    if OrderDbQueries().fetch_order(user_info["email"], menu_id):
                        print(OrderDbQueries().fetch_order(user_info["email"], menu_id))
                        return{"response":"successfuly placed food order"}
                    return{"response":"order not successful"}
                except:
                    return{"response":"menu doesnt exist"}
            return{"response":"not authenticated"}
        return {"response":"empty fields"}
