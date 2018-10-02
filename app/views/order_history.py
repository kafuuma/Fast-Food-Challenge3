from flask import  request
from flask_restful import Resource
from app.models.validate import VerifyOrders, VerifyToken
from app.models.orders import Orders
from app.models.db_actions import OrderDbQueries

class UserOrderHistory(Resource):
    def get(self):
        auth_token = request.headers["Authentication"]
        user_info = VerifyToken.validate(auth_token)
        if user_info:
            response = OrderDbQueries().fetch_orders(user_info["email"])
            if response:
                return{"response":response}
            return{"response":"no orders for {}".format(user_info["email"])}
        return{"response":"not authenticated"}
    