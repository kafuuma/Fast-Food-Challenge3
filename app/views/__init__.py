from flask_restful import Resource, Api
from flask import jsonify
from app.views.signup import Signup
from app.views.login import Login
from app.views.add_menu import AddMenu
from app.views.get_menu import GetMenu
from app.views.place_order import PlaceOrders
from app.views.update_status import UpdateOrderStatus
from app.views.order_history import UserOrderHistory
from app.views.fetch_order import FetchSpecificOrder
from app.views.fectch_all_orders import GetAllOrders
from app.models.users import Users
from app.models.db_actions import MenuDbQueries, UserDbQueries, OrderDbQueries
from app import app


import os

app.config["SECRET_KEY"] = os.getenv('SECRET')
api = Api(app)

dbuser = UserDbQueries()
dbuser.create_table()
dbmenu = MenuDbQueries()
dbmenu.create_table()
dborder = OrderDbQueries()
dborder.create_table()
supper_user = Users("super@email.com","password@super","super","078808881","admin")
if not supper_user.login():
    supper_user.signup()

api.add_resource(Signup, "/api/v1/auth/signup")
api.add_resource(Login, "/api/v1/auth/login")
api.add_resource(AddMenu, "/api/v1/menu")
api.add_resource(GetMenu, "/api/v1/menu")
api.add_resource(PlaceOrders, "/api/v1/users/orders")
api.add_resource(UpdateOrderStatus, "/api/v1/orders/<int:order_id>")
api.add_resource(UserOrderHistory, "/api/v1/users/orders")
api.add_resource(FetchSpecificOrder, "/api/v1/orders/<int:order_id>")
api.add_resource(GetAllOrders, "/api/v1/orders")


