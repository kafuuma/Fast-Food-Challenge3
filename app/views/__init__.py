from flask_restful import Resource, Api
from signup import Signup
from login import Login
from add_menu import AddMenu
from get_menu import GetMenu
from place_order import PlaceOrders
from update_status import UpdateOrderStatus
from app import app
import os

app.config["SECRET_KEY"] = "topsecretlevel2000classified"
api = Api(app)



api.add_resource(Signup, "/api/v1/auth/signup")
api.add_resource(Login, "/api/v1/auth/login")
api.add_resource(AddMenu, "/api/v1/menu")
api.add_resource(GetMenu, "/api/v1/menu")
api.add_resource(PlaceOrders, "/api/v1/users/orders")
api.add_resource(UpdateOrderStatus, "/api/v1/orders/<int:order_id>")

