from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from controllers.auth_middleware import token_required

# Blueprint tanımı
network_bp = Blueprint("network", __name__, url_prefix="/network")
network_api = Api(network_bp)

# Swagger Model Tanımı
network_model = network_api.model("NetworkConnection", {
    "id": fields.Integer(description="Bağlantı ID", example=1),
    "name": fields.String(description="Bağlantının Adı", example="Alice Johnson"),
    "job": fields.String(description="Bağlantının Mesleği", example="Software Engineer"),
    "mutual_connection": fields.String(description="Ortak Bağlantı Sayısı", example="5 mutual friends"),
    "date": fields.String(description="Süre", example="2h"),
    "profile_image": fields.String(description="Profil Resmi URL", example="https://example.com/image.jpg"),
    "is_approved": fields.Boolean(description="Bağlantı Onayı", example=True)
})

network_connections = [
      {
        "id": 1,
        "name": "Mevsim Gediz",
        "job": "iOS Developer",
        "date": "2m",
        "mutual_connection": "15 mutual connections",
        "profile_image": "http://127.0.0.1:5003/images/mevsim.jpg",
        "is_approved": True
    },
    {
        "id": 2,
        "name": "Alice Johnson",
        "job": "Software Engineer",
        "mutual_connection": "10 mutual connections",
        "date": "2h",
        "profile_image": "http://127.0.0.1:5003/images/alice.jpg",
        "is_approved": True
    },
    {
        "id": 3,
        "name": "Bob Smith",
        "job": "Data Analyst",
        "date": "2h",
        "mutual_connection": "5 mutual connections",
        "profile_image": "http://127.0.0.1:5003/images/bob.jpg",
        "is_approved": True
    },
     {
        "id": 4,
        "name": "Cihan Kutlu",
        "job": "Android Developer",
        "date": "10h",
        "mutual_connection": "2 mutual connections",
        "profile_image": "http://127.0.0.1:5003/images/cihan.jpg",
        "is_approved": True
    } ,
     {
        "id": 4,
        "name": "Metehan Sayan",
        "job": "Data Analyst",
        "date": "10h",
        "mutual_connection": "1 mutual connections",
        "profile_image": "http://127.0.0.1:5003/images/metehan.jpg",
        "is_approved": True
    } ,
     {
        "id": 5,
        "name": "Aslıhan Korkmaz",
        "job": "AI Engineer",
        "date": "3h",
        "mutual_connection": "20 mutual connections",
        "profile_image": "http://127.0.0.1:5003/images/aslihan.jpg",
        "is_approved": True
    } 
]

SECRET_KEY = "your_secret_key"



@network_api.route("/list")
class NetworkListResource(Resource):
    @network_api.marshal_list_with(network_model)
    @network_api.response(200, "Başarılı")
    @token_required
    def post(self):
        """Kullanıcının tüm bağlantılarını getir"""
        return network_connections

@network_api.route("/add_connection")
class AddConnectionResource(Resource):
    @network_api.expect(network_model, validate=True)
    @token_required
    def post(self):
        """Yeni bağlantı ekle"""
        data = request.get_json()
        new_id = max([c["id"] for c in network_connections], default=0) + 1
        new_connection = {"id": new_id, **data}
        network_connections.append(new_connection)
        return {"message": "Connection added", "connection": new_connection}, 201

@network_api.route("/reject_connection")
class RejectConnectionResource(Resource):
    @network_api.expect(fields.String(required=True, description="Bağlantının Adı", example="Alice Johnson"))
    @token_required
    def post(self):
        """Bağlantıyı reddet"""
        data = request.get_json()
        name = data.get("name")
        connection = next((c for c in network_connections if c["name"] == name), None)
        
        if connection:
            network_connections.remove(connection)
            return {"message": "Connection removed", "connection": connection}, 200
        else:
            return {"error": "Connection not found"}, 404
