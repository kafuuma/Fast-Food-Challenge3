from flask import request
from flask_restful import Resource
from app.models.validate import VerifyMenu, VerifyToken
from app.models.menu import Menu
from app.models.db_actions import MenuDbQueries

class AddMenu(Resource):
    """
    This class inherits from the resource class and implements 
    an api end point to add menu 
    """
    def post(self):
        user_request = request.get_json()
        if user_request:
            menu_name = user_request.get("menu_name")
            menu_descrpn = user_request.get("description")
            menu_price = user_request.get("menu_price")
            menu_image = user_request.get("image")
            auth_token = request.headers["Authentication"]
            user_info = VerifyToken.validate(auth_token)
            valid = VerifyMenu(menu_name,menu_descrpn,menu_price)
            if user_info:
                if valid.check_if_empty():
                    if not valid.check_menu_price():
                        return {"message":"menu_price must be digits"},400
                    if user_info["user_role"] == "admin":
                        menu = Menu(menu_name, menu_descrpn, menu_price, menu_image)
                        try:
                            menu.add_menu_item()
                            if MenuDbQueries().fetch_menu(menu):
                                return{"message":"menu successfuly created"},201
                            return {"message":"unsuccessful, server error"},500
                        except:
                            return {"message":"menu_exists"},409
                    return{"message":"Only admins create menu items"},401
                return{"message":"empty inputs"},400
            return {"message":"Not Authenticated"},401
        return {"message":"empty fields"},400


