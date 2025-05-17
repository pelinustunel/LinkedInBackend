from flask import Blueprint
from flask_restx import Api, Resource, fields
from models.post_model import Post
from controllers.auth_middleware import token_required
from controllers.post_controller import get_all_posts 

# Blueprint tanımı
home_bp = Blueprint("home", __name__, url_prefix="/home")
home_api = Api(home_bp)

# Dummy veri listesi
posts = []

# Swagger için Post modeli
post_model = home_api.model("Post", {
    "post_id": fields.Integer(description="Post ID", example=1),
    "user_id": fields.String(description="Kullanıcı ID", example="123"),
    "content": fields.String(description="Gönderi İçeriği", example="Bugün çok güzel bir gün!"),
    "image_url": fields.String(description="Gönderiye ait resim URL", example="https://example.com/image.jpg"),
    "timestamp": fields.String(description="Gönderi Zamanı", example="2025-02-23 14:00:00"),
    "likes": fields.Integer(description="Beğeni sayısı", example=0),
    "comments": fields.List(fields.String, description="Yorumlar", example=["Harika!", "Tebrikler!"])
})

@home_api.route("/feed")
class HomeFeed(Resource):
    @home_api.marshal_list_with(post_model)
    @token_required
    def post(self):
        """Ana sayfada gösterilecek gönderileri getir"""
        return [p.to_dict() for p in get_all_posts()]  # Artık asıl post listesini kullanır
