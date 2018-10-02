from flask import request, jsonify
from flask_restful import Resource
from jwt import encode
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.validate import VerifyUsers
from app.models.users import Users
from app.models.db_actions import UserDbQueries
from app import app


class Login(Resource):
    def post(self):
        user_request = request.get_json()
        email = user_request.get("email")
        password = user_request.get("password")
        if user_request:
            user = Users(email, password).login()
            if user:
                if check_password_hash(user.password, password):
                    auth_token = encode(
                        {"email":user.email, "password":user.password, "user_role":user.user_role},
                        app.config["SECRET_KEY"]
                    )
                    return {"Authentication": auth_token.decode("UTF-8")},200
                return {"response":"wrong password"},401
            return {"response":"User doesnt exist"}, 400
        return {"response":"empty fields"}, 409