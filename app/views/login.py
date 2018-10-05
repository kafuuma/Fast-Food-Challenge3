from flask import request, jsonify
from flask_restful import Resource
from jwt import encode
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.validate import VerifyUsers
from app.models.users import Users
from app.models.db_actions import UserDbQueries
from app import app


class Login(Resource):
    """
    This class inherits from the resource class 
    and implements an end point to login into 
    the application
    """
    def post(self):
        user_request = request.get_json()
        email = str(user_request.get("email"))
        password = str(user_request.get("password"))
        if user_request:
            user = Users(email, password).login()
            if user:
                if check_password_hash(user.password, password):
                    auth_token = encode(
                        {"email":user.email, "password":user.password, "user_role":user.user_role},
                        app.config["SECRET_KEY"]
                    )
                    return {    
                                "message":"login successfull",
                                "Authentication": auth_token.decode("UTF-8")
                            },200
                return {"message":"wrong password"},401
            return {"message":"User doesnt exist"}, 400
        return {"message":"empty fields"}, 409