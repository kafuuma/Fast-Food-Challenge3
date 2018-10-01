from flask_restful import Resource, Api
from signup import Signup
from app import app
import os

app.config["SECRET_KEY"] = os.getenv('SECRET')
api = Api(app)



api.add_resource(Signup, "/api/v1/auth/signup")