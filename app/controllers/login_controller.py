# login_controller.py
import jwt
import datetime
from flask import Blueprint, request
from flask_restx import Api, Resource, fields

SECRET_KEY = "your_secret_key"

# URL prefix burada anlamlı: "/login"
login_bp = Blueprint("login", __name__, url_prefix="/login")
login_api = Api(login_bp)

# Swagger Model
login_model = login_api.model("Login", {
    "username": fields.String(required=True, description="Kullanıcı Adı", example="testuser"),
    "password": fields.String(required=True, description="Şifre", example="password123"),
})

@login_api.route("/")
class LoginResource(Resource):
    @login_api.expect(login_model)
    @login_api.response(200, "Login Successful")
    @login_api.response(401, "Invalid Credentials")
    def post(self):
        """Kullanıcı giriş işlemi ve JWT token oluşturma"""
        data = request.get_json()

        if not data or "username" not in data or "password" not in data:
            return {"error": "Eksik bilgi girdiniz."}, 400

        username = data["username"]
        password = data["password"]
        
        if username == "pelin@gmail.com" and password == "123":
            access_token = jwt.encode(
                {
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            refresh_token = jwt.encode(
                {
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            user_id = "2"
            user_name = "Pelin Üstünel"

            return {
                "message": "Giriş başarılı!",
                "token": access_token,
                "refresh_token": refresh_token,  # ✅ bu eklendi
                "user_id": user_id,
                "user_name": user_name
        }, 200

        return {"error": "Geçersiz kimlik bilgileri"}, 401

@login_api.route("/refresh")
class RefreshTokenResource(Resource):
    @login_api.doc(params={"refresh_token": "Geçerli refresh token"})
    @login_api.response(200, "Token yenilendi")
    @login_api.response(401, "Refresh token geçersiz veya süresi dolmuş")
    def post(self):
        """Refresh token ile yeni access token üret"""
        data = request.get_json()
        refresh_token = data.get("refresh_token")

        if not refresh_token:
            return {"message": "Refresh token gönderilmedi!"}, 400

        try:
            decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            username = decoded["username"]

            new_access_token = jwt.encode(
                {
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            return {"token": new_access_token}, 200

        except jwt.ExpiredSignatureError:
            return {"message": "Refresh token süresi dolmuş!"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Geçersiz refresh token!"}, 401
