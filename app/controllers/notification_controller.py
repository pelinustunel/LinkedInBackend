from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from controllers.auth_middleware import token_required
from models.notification_model import Notification

SECRET_KEY = "your_secret_key"

# Blueprint tanımı
notification_bp = Blueprint("notification", __name__, url_prefix="/notification")
notification_api = Api(notification_bp)

# Swagger Model Tanımı
notification_model = notification_api.model("Notification", {
    "notification_id": fields.Integer(description="Bildirim ID", example=1),
    "user_id": fields.Integer(description="Kullanıcı ID", example=1),
    "notification_image": fields.String(description="Profil Resmi", example="http://127.0.0.1:5003/images/profile.jpg"),
    "message": fields.String(description="Bildirim Mesajı", example="Alice sent you a connection request"),
    "timestamp": fields.String(description="Zaman", example="2h")
})


notifications = [
    Notification(notification_id=1, user_id=1, notification_image="http://127.0.0.1:5003/images/mevsim.jpg", message="Mevsim Gediz sent you a connection request", timestamp="1h"),
    Notification(notification_id=2, user_id=2, notification_image="http://127.0.0.1:5003/images/aslihan.jpg", message="Aslıhan Korkmaz liked your post", timestamp="2h"),
    Notification(notification_id=3, user_id=3, notification_image="http://127.0.0.1:5003/images/cihan.jpg", message="Cihan Kutlu commented: 'Great insight!'", timestamp="6h"),
    Notification(notification_id=4, user_id=4, notification_image="http://127.0.0.1:5003/images/metehan.jpg", message="Metehan Sayan started following you", timestamp="7h"),
    Notification(notification_id=5, user_id=5, notification_image="http://127.0.0.1:5003/images/pelin.jpg", message="Pelin Üstünel endorsed you for Swift", timestamp="22h"),
    Notification(notification_id=6, user_id=1, notification_image="http://127.0.0.1:5003/images/mevsim.jpg", message="Mevsim Gediz mentioned you in a comment", timestamp="1d"),
    Notification(notification_id=7, user_id=3, notification_image="http://127.0.0.1:5003/images/cihan.jpg", message="Cihan Kutlu shared your post", timestamp="2d"),
    Notification(notification_id=8, user_id=4, notification_image="http://127.0.0.1:5003/images/metehan.jpg", message="Metehan Sayan viewed your profile", timestamp="3d"),
    Notification(notification_id=9, user_id=2, notification_image="http://127.0.0.1:5003/images/aslihan.jpg", message="Aslıhan Korkmaz invited you to join iOS Developers Group", timestamp="4d"),
    Notification(notification_id=10, user_id=5, notification_image="http://127.0.0.1:5003/images/pelin.jpg", message="Pelin Üstünel sent you a message: 'Let's connect!'", timestamp="5d")
]


#  Tüm bildirimleri getir (POST notifications/list)
@notification_api.route("/list")
class NotificationListResource(Resource):
    @notification_api.marshal_list_with(notification_model)
    @notification_api.response(200, "Başarılı")
    @token_required  
    def post(self):
        """Tüm bildirimleri getir (Giriş yapmış kullanıcılar için)"""
        return notifications

#  Bildirim silme (DELETE notifications/{notification_id})
@notification_api.route("/<int:notification_id>")
@notification_api.param("notification_id", "Silinecek Bildirim ID")
class NotificationResource(Resource):
    @notification_api.response(200, "Bildirim silindi")
    @notification_api.response(404, "Bildirim bulunamadı")
    @token_required
    def delete(self, notification_id):
        """Belirtilen bildirimi sil (Giriş yapmış kullanıcılar için)"""
        global notifications
        # Bildirimin var olup olmadığını kontrol et
        matching = [n for n in notifications if n.notification_id == notification_id]
        if not matching:
            return {"error": "Notification not found"}, 404
        
        # Silme işlemini yap
        notifications = [n for n in notifications if n.notification_id != notification_id]
        return {"message": "Notification deleted"}, 200
