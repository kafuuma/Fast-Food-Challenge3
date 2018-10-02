from flask_restful import Resource, Api
from signup import Signup
from login import Login
from app import app
import os

app.config["SECRET_KEY"] = "topsecretlevel2000classified"
api = Api(app)



api.add_resource(Signup, "/api/v1/auth/signup")
api.add_resource(Login, "/api/v1/auth/login")