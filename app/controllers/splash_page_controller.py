from flask import Blueprint,request
from flask_restx import Api, Resource
from controllers.auth_middleware import token_required  

SECRET_KEY = "your_secret_key"

# Blueprint tanımı
splash_bp = Blueprint("splash", __name__, url_prefix="/splash")
splash_api = Api(splash_bp)


@splash_api.route("/")
class SplashResource(Resource):
    @token_required  
    def post(self):
        """Splash Page - Kullanıcı giriş yapmış mı kontrol edilir"""
        username = request.user["username"]  
        return {"redirect": "/home", "message": f"Hoş geldin, {username}!"}, 200