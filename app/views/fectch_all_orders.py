from flask import request
from flask_restful import Resource
from app.models.validate import VerifyOrders, VerifyToken
from app.models.orders import Orders
from app.models.db_actions import OrderDbQueries

class GetAllOrders(Resource):
    def get(self):
        auth_token = request.headers["Authentication"]
        user_info = VerifyToken.validate(auth_token)
        if user_info:
            if user_info["user_role"] == "admin":
                response = OrderDbQueries().fetch_all_orders()
                return {"response": response}
            return {"response":"only admins have access all orders"}
        return{"response":"not authinticated"}