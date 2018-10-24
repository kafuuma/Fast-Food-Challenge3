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
            status = user_request.get("status")
            valid = VerifyOrders(order_id, status)
            if user_info:
                if valid.check_order():
                    if user_info["user_role"] == "admin":
                        if OrderDbQueries().fetch_order_byId(order_id):
                            try:
                                OrderDbQueries().update_order_status(int(order_id),status)
                                return{"message":"order status updated successfuly"},201
                            except:
                                return{"message":"{} is not valid input".format(status)},500
                        return{"message":"order doesn't exist"},404
                    return{"message":"not authenticated"},401
                return {"message":"status must not be empty"},400
        return{"message":"empty fields"},400