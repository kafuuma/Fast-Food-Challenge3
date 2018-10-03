from flask import request
from flask_restful import Resource
from app.models.validate import VerifyOrders, VerifyToken
from app.models.orders import Orders
from app.models.db_actions import OrderDbQueries

class UpdateOrderStatus(Resource):
    """This class inherits from a resource class,
    it implements an end point for updating order status"""
    def put(self, order_id):
        user_request = request.get_json()
        if user_request:
            auth_token = request.headers["Authentication"]
            user_info = VerifyToken.validate(auth_token)
            if user_info:
                if user_info["user_role"] == "admin":
                    status = user_request.get("status")
                    if OrderDbQueries().fetch_order_byId(order_id):
                        try:
                            OrderDbQueries().update_order_status(int(order_id),status)
                            return{"message":"order status updated to {}".format(status)}
                        except:
                            return{"message":"{} is not valid input".format(status)}
                    return{"message":"order doesn't exist"}
            return{"message":"not authenticated"}
        return{"message":"empty fields"}