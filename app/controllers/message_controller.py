from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from models.message_storage import messages, get_next_message_id
from models.message_model import Message
from controllers.auth_middleware import token_required
from datetime import datetime

message_bp = Blueprint("message", __name__, url_prefix="/message")
message_api = Api(message_bp)

message_model = message_api.model("Message", {
    "message_id": fields.Integer(description="Mesaj ID", example=1),
    "sender_id": fields.String(required=True, description="Gönderen Kullanıcı ID", example="1"),
    "sender_name": fields.String(required=True, description="Gönderen Kullanıcı Adı", example="Mevsim Gediz"),         # ✅ EKLENDİ
    "sender_image": fields.String(required=True, description="Gönderen Kullanıcı Resmi", example="https://example.com/sender.png"),
    "receiver_id": fields.String(required=True, description="Alıcı Kullanıcı ID", example="2"),
    "receiver_name": fields.String(required=True, description="Alıcı Kullanıcı Adı", example="Pelin Üstünel"),          # ✅ EKLENDİ
    "receiver_image": fields.String(required=True, description="Alıcı Kullanıcı Resmi", example="https://example.com/receiver.png"),
    "content": fields.String(required=False, description="Mesaj İçeriği", example="Merhaba!"),
    "image_url": fields.String(required=False, description="Mesajla gönderilen resmin URL'si", example="https://example.com/image.png"),
    "timestamp": fields.String(description="Gönderim Zamanı", example="2025-02-22")
})

conversation_model = message_api.model("Conversation", {
    "other_user_id": fields.String(required=True, description="Diğer Kullanıcı ID", example="1"),
    "other_user_name": fields.String(required=True, description="Diğer Kullanıcı Adı", example="Mevsim Gediz"),
    "other_user_image": fields.String(required=True, description="Diğer Kullanıcı Resmi", example="https://example.com/image.png"),
    "last_message": fields.String(required=True, description="Son Mesaj İçeriği", example="Merhaba!"),
    "last_message_time": fields.String(required=True, description="Son Mesaj Zamanı", example="2025-02-22")
})

detail_request_model = message_api.model("DetailRequestModel", {
    "current_user_id": fields.String(required=True, description="Giriş yapan kullanıcının ID'si", example="2"),
    "other_user_id": fields.String(required=True, description="Sohbet geçmişi istenen diğer kullanıcının ID'si", example="1")
})


# ✅ Gelen POST body için model (sadece user_id)
user_id_model = message_api.model("UserIdModel", {
    "user_id": fields.String(required=True, description="Mesajları listelenecek kullanıcı ID", example="2")
})

SECRET_KEY = "your_secret_key"

@message_api.route("/list")
class MessageListResource(Resource):
    @message_api.expect(user_id_model, validate=True)
    @message_api.response(200, "Başarılı", [conversation_model])
    @token_required
    def post(self):
        """Kullanıcının diğer kişilerle olan son mesajlarını getirir (POST)"""
        data = request.get_json()
        user_id = data.get("user_id")

        conversations = {}

        for msg in messages:
            if msg.sender_id == user_id:
                other_id = msg.receiver_id
                other_name = msg.receiver_name
                other_image = msg.receiver_image
            elif msg.receiver_id == user_id:
                other_id = msg.sender_id
                other_name = msg.sender_name
                other_image = msg.sender_image
            else:
                continue

            key = other_id
            current_timestamp = datetime.strptime(msg.timestamp, "%Y-%m-%d")

            if key not in conversations or current_timestamp > datetime.strptime(conversations[key]["last_message_time"], "%Y-%m-%d"):
                conversations[key] = {
                    "other_user_id": other_id,
                    "other_user_name": other_name,
                    "other_user_image": other_image,
                    "last_message": msg.content,
                    "last_message_time": msg.timestamp
                }

        return list(conversations.values()), 200

@message_api.route("/send_message")
class SendMessageResource(Resource):
    @message_api.expect(message_model)
    @message_api.response(201, "Mesaj başarıyla oluşturuldu", message_model)
    @token_required
    def post(self):
        """Yeni mesaj gönder"""
        data = request.get_json()
        new_id = get_next_message_id()

        new_message = Message(
            message_id=new_id,
            sender_id=data["sender_id"],
            sender_name=data["sender_name"],                         
            sender_image=data["sender_image"],
            receiver_id=data["receiver_id"],
            receiver_name=data["receiver_name"],                      
            receiver_image=data["receiver_image"],
            content=data.get("content", ""),
            image_url=data.get("image_url", ""),
            timestamp=data["timestamp"]
        )

        messages.append(new_message)
        return new_message.to_dict(), 201

@message_api.route("/<int:message_id>")
@message_api.doc(params={"message_id": "Getirmek istediğiniz mesajın ID'si"})
class MessageDetailResource(Resource):
    @message_api.response(200, "Başarılı", message_model)
    @message_api.response(404, "Mesaj Bulunamadı")
    @token_required
    def post(self, message_id):
        """Belirli bir mesajı getir (POST yöntemi ile)"""
        message = next((msg for msg in messages if msg.message_id == message_id), None)
        if message:
            return message.to_dict(), 200
        return {"error": "Message not found"}, 404

@message_api.route("/detail")
class MessageDetailHistoryResource(Resource):
    @message_api.expect(detail_request_model, validate=True)
    @message_api.response(200, "Başarılı", [message_model])
    @token_required
    def post(self):
        """İki kullanıcı arasındaki tüm mesaj geçmişini getirir"""
        data = request.get_json()
        current_user_id = data.get("current_user_id")
        other_user_id = data.get("other_user_id")

        # Bu iki kullanıcı arasındaki mesajları filtrele
        chat_history = [
            msg.to_dict() for msg in messages
            if (msg.sender_id == current_user_id and msg.receiver_id == other_user_id)
            or (msg.sender_id == other_user_id and msg.receiver_id == current_user_id)
        ]

        # Mesajları tarihe göre sıralayalım (eski → yeni)
        chat_history.sort(key=lambda x: x["timestamp"])

        return chat_history, 200
