from flask import request
from flask_restful import Resource
from app.models.validate import VerifyOrders, VerifyToken
from app.models.orders import Orders
from app.models.db_actions import OrderDbQueries

class FetchSpecificOrder(Resource):
    """
    This class implements and point to fetch a specific
    order by id
    """
    def get(self, order_id):
        auth_token = request.headers["Authentication"]
        user_info = VerifyToken.validate(auth_token)
        if user_info:
            if user_info["user_role"] == "admin":
                response = OrderDbQueries().fetch_order_byId(int(order_id))
                return {
                        "order":response,
                        "message":"successfully fetched order"
                        },200
            return {"message":" only admins access this resource"},404
        return {"message":"not authenticated"},404
     