from flask import request
from flask_restful import Resource
from app.models.validate import VerifyMenu, VerifyToken
from app.models.menu import Menu
from app.models.db_actions import MenuDbQueries

class AddMenu(Resource):
    def post(self):
        user_request = request.get_json()
        print(user_request)
        if user_request:
            menu_name = user_request.get("menu_name")
            menu_descrpn = user_request.get("description")
            menu_price = user_request.get("menu_price")
            auth_token = request.headers["Authentication"]
            print(auth_token)
            user_info = VerifyToken.validate(auth_token)
            print(user_info)
            if user_info:
                if user_info["user_role"] == "admin":
                    menu = Menu(menu_name, menu_descrpn, menu_price)
                    try:
                        menu.add_menu_item()
                        if MenuDbQueries().fetch_menu(menu):
                            print(MenuDbQueries().fetch_menu(menu))
                            return{"response":"menu successfuly created"},201
                        return {"response":"unsuccessful, server error"},400
                    except:
                        return {"response":"menu_exists"},409
                return{"response":"Only admins create menu items"},401
            return {"response":"Not Authenticated"}
        return {"response":"empty fields"},400

"""
api.add_resource(AddMenu, "/api/v1/menu")
"""
