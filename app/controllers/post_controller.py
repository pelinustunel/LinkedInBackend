from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from models.post_model import Post
from controllers.auth_middleware import token_required
import os
from datetime import datetime
from flask import current_app

# Blueprint tanımı
post_bp = Blueprint("post", __name__, url_prefix="/post")
post_api = Api(post_bp)

# Mock post listesi (Post objeleri olarak)
posts = [   
    Post(
        post_id=1,
        user_id="Pelin Üstünel",
        content="Yeni projemi bitirdim.",
        image_url="http://127.0.0.1:5003/images/iosUIPost.jpg",
        profile_image_url="http://127.0.0.1:5003/images/pelin.jpg",
        job_text = "iOS Developer",
        timestamp="2025-04-20 10:30:00",
        likes=350,
        comments=["Çok güzel!", "Katılıyorum!"]
    ),
    
    Post(
        post_id=2,
        user_id="Mevsim Gediz",
        content="Yeni ekip yeni başlangıçlar 🎉",
        image_url= "http://127.0.0.1:5003/images/groupPost.jpg",
        profile_image_url = "http://127.0.0.1:5003/images/mevsim.jpg",
        job_text = "Software Engineer",
        timestamp="2025-04-18 08:00:00",
        likes=200,
        comments=["Kesinlikle!", "Aynı fikirdeyim."]
    ),

    Post(
        post_id=3,
        user_id="Cihan Kutlu",
        content="Yeni bootcamp'imi size duyurmaktan mutluluk duyarım.",
        image_url= "http://127.0.0.1:5003/images/iosBootcamp.jpg",
        profile_image_url = "http://127.0.0.1:5003/images/cihan.jpg",
        job_text = "Software Engineer",
        timestamp="2025-04-18 08:00:00",
        likes=200,
        comments=["Kesinlikle!", "Aynı fikirdeyim."]
    ),


    Post(
        post_id=4,
        user_id="Metehan Sayan",
        content="Kahveyle güne başlamak gibisi yok ☕",
        image_url= "http://127.0.0.1:5003/images/desk.jpg",
        profile_image_url = "http://127.0.0.1:5003/images/metehan.jpg",
        job_text = "Software Engineer",
        timestamp="2025-04-18 08:00:00",
        likes=200,
        comments=["Kesinlikle!", "Aynı fikirdeyim."],
    ),
    
    Post(
        post_id=3,
        user_id="Aslıhan Korkmaz",
        content="Yeni projemi paylaştım! 🎉",
        image_url="http://127.0.0.1:5003/images/androidUI.png",
        profile_image_url="http://127.0.0.1:5003/images/aslihan.jpg",
        job_text = "Software Engineer",
        timestamp="2025-04-19 15:45:00",
        likes=150,
        comments=["Eline sağlık", "Tebrikler!", "Link var mı?"]
    )
  
    ]

# Swagger Model Tanımları
post_model = post_api.model("Post", {
    "user_id": fields.String(required=True, description="Kullanıcı ID", example="123"),
    "content": fields.String(required=True, description="Gönderi metni", example="Yeni gönderi"),
    "image_url": fields.String(required=False, description="Gönderi görseli", example="https://example.com/image.jpg"),
    "profile_image_url": fields.String(required=False, description="Profil resmi", example="https://example.com/profile.jpg"),
    "job_text": fields.String(required=False, description="Meslek bilgisi", example="iOS Developer"),
    "timestamp": fields.String(required=False, description="Zaman damgası", example="2025-02-23 14:00:00"),
    "likes": fields.Integer(required=False, description="Beğeni sayısı", example=0),
    "comments": fields.List(fields.String, required=False, description="Yorumlar")
})


post_response_model = post_api.inherit("PostResponse", post_model, {
    "post_id": fields.Integer(description="Post ID", example=1),
})

message_model = post_api.model("Message", {
    "message": fields.String(description="Bilgilendirme mesajı", example="Post deleted")
})

def get_all_posts():
    return posts


# Tüm postları getir (GET /post/list)
@post_api.route("/list")
class PostListResource(Resource):
    @post_api.marshal_with(post_response_model, as_list=True)
    @token_required
    def post(self):
        """Tüm gönderileri getir"""
        return [p.to_dict() for p in posts], 200

@post_api.route("/add_post")
class AddPostResource(Resource):
    @token_required
    def post(self):
        print("📦 request.content_type:", request.content_type)
        print("📄 Form Verisi:", request.form)
        print("🖼️ Dosya Verisi:", request.files)

        user_id = request.form.get("user_id", "Unknown User")
        content = request.form.get("content")
        image_file = request.files.get("image")

        if not content:
            return {"error": "Content field is required."}, 400

        image_url = None
        if image_file and image_file.filename != "":
            filename = f"{int(datetime.now().timestamp())}_{image_file.filename}"
            image_folder = os.path.join(os.path.dirname(__file__), '..', 'images')
            image_folder = os.path.abspath(image_folder)
            os.makedirs(image_folder, exist_ok=True)

            image_path = os.path.join(image_folder, filename)
            image_file.save(image_path)

            image_url = f"http://127.0.0.1:5003/images/{filename}"

        new_id = max([p.post_id for p in posts], default=0) + 1
        new_post = Post(
            post_id=new_id,
            user_id=user_id,
            content=content,
            image_url=image_url,
            profile_image_url=None,
            job_text=None,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            likes=0,
            comments=[]
        )
        posts.append(new_post)
        return {"message": "Post created"}, 201

# Post güncelle (PUT /post/update_post/<post_id>)
@post_api.route("/update_post/<int:post_id>")
class UpdatePostResource(Resource):
    @post_api.expect(post_model)
    @post_api.marshal_with(post_response_model)
    @post_api.response(404, "Post not found")
    @token_required
    def put(self, post_id):
        """Post güncelle"""
        data = request.get_json()
        for post in posts:
            if post.post_id == post_id:
                post.user_id = data.get("user_id", post.user_id)
                post.content = data.get("content", post.content)
                post.image_url = data.get("image_url", post.image_url)
                post.timestamp = data.get("timestamp", post.timestamp)
                post.likes = data.get("likes", post.likes)
                post.comments = data.get("comments", post.comments)
                return post.to_dict(), 200
        return {"error": "Post not found"}, 404

# Post sil (DELETE /post/delete_post/<post_id>)
@post_api.route("/delete_post/<int:post_id>")
class DeletePostResource(Resource):
    @post_api.marshal_with(message_model)
    @post_api.response(404, "Post not found")
    @token_required
    def delete(self, post_id):
        """Post sil"""
        global posts
        post = next((p for p in posts if p.post_id == post_id), None)

        if not post:
            return {"error": "Post not found"}, 404

        posts = [p for p in posts if p.post_id != post_id]
        return {"message": "Post deleted"}, 200
    

