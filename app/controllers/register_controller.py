from flask import Blueprint
from flask_restx import Api, Resource, fields

# Blueprint tanımı
register_bp = Blueprint("register", __name__, url_prefix="/register")
register_api = Api(register_bp)

# Swagger Model Tanımı
register_model = register_api.model("Register", {
    "first_name": fields.String(required=True, description="Ad", example="John"),
    "last_name": fields.String(required=True, description="Soyad", example="Doe"),
    "email": fields.String(required=True, description="E-posta adresi", example="johndoe@example.com"),
    "password": fields.String(required=True, description="Şifre", example="securepassword123"),
})

response_model = register_api.model("RegisterResponse", {
    "message": fields.String(description="Sonuç mesajı", example="User registered successfully"),
})

@register_api.route("")
class RegisterResource(Resource):
    @register_api.expect(register_model)
    @register_api.marshal_with(response_model, code=201)
    @register_api.response(400, "Invalid input")
    def post(self):
        """Yeni kullanıcı kaydı oluştur"""
        data = register_api.payload
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")

        if first_name and last_name and email and password:
            return {"message": "User registered successfully"}, 201
        return {"error": "Invalid input"}, 400

