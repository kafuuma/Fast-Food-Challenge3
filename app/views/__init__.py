from flask_restful import Resource, Api
from signup import Signup
from login import Login
from add_menu import AddMenu
from get_menu import GetMenu
from place_order import PlaceOrders
from update_status import UpdateOrderStatus
from order_history import UserOrderHistory
from fetch_order import FetchSpecificOrder
from fectch_all_orders import GetAllOrders
from app import app
import os

app.config["SECRET_KEY"] = os.getenv('SECRET')
api = Api(app)



api.add_resource(Signup, "/api/v1/auth/signup")
api.add_resource(Login, "/api/v1/auth/login")
api.add_resource(AddMenu, "/api/v1/menu")
api.add_resource(GetMenu, "/api/v1/menu")
api.add_resource(PlaceOrders, "/api/v1/users/orders")
api.add_resource(UpdateOrderStatus, "/api/v1/orders/<int:order_id>")
api.add_resource(UserOrderHistory, "/api/v1/users/orders")
api.add_resource(FetchSpecificOrder, "/api/v1/orders/<int:order_id>")
api.add_resource(GetAllOrders, "/api/v1/orders")


