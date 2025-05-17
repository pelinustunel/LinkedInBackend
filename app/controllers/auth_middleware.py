import jwt
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "your_secret_key"

EXCLUDED_PATHS = ["/login", "/swagger"]  # Token gerekmeyen endpoint'ler

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.path in EXCLUDED_PATHS:  # Eğer hariç tutulan bir endpoint ise, devam et
            return f(*args, **kwargs)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token bulunamadı!"}), 401

        token = auth_header.replace("Bearer ", "").strip()
        
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token  
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token süresi dolmuş!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Geçersiz token!"}), 401

        return f(*args, **kwargs)
    return decorated
