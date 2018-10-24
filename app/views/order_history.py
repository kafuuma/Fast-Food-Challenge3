from flask import  request
from flask_restful import Resource
from app.models.validate import VerifyOrders, VerifyToken
from app.models.orders import Orders
from app.models.db_actions import OrderDbQueries

class UserOrderHistory(Resource):
    """
    This class inherits from the  resource class and 
    implements an end point for the user to view their
    order history
    """
    def get(self):
        auth_token = request.headers["Authentication"]
        user_info = VerifyToken.validate(auth_token)
        if user_info:
            response = OrderDbQueries().fetch_orders(user_info["email"])
            if response:
                 return{"message":"successfully fetched orders",
                        "orders":response},200
            return{"message":"no orders for you"},404
        return{"message":"not authenticated"},401
    