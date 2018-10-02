from flask import request
from flask_restful import Resource
from app.models.validate import VerifyUsers
from app.models.users import Users
from app.models.db_actions import UserDbQueries

class Signup(Resource):
    def post(self):
        user_request = request.get_json()
        username = user_request.get("full_name")
        password = user_request.get("password")
        email = user_request.get("email")
        contact = user_request.get("contact")
        user_role = user_request.get("user_role")
        confirm_password = user_request.get("confirm_password")
        if user_request:
            if password == confirm_password:
                try:
                    Users(email, password, username, contact, user_role).signup()
                    if Users(email, password).login():
                        return {"response":"signup successfull"}, 201
                    return {"response":"signup not successful"}, 500
                except:
                    return {"response":"user exists"},409
            return {"response": "Passwords do not match"}, 401
        return {"response": "Fields Empty"}, 400


