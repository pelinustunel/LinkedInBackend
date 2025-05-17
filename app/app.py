from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_compress import Compress

def create_app():
    app = Flask(__name__)
    
    # CORS ve Gzip aktif
    CORS(app)
    Compress(app)

    # Blueprint importları
    from controllers.home_controller import home_bp
    from controllers.jobs_controller import job_bp
    from controllers.login_controller import login_bp
    from controllers.message_controller import message_bp
    from controllers.my_network_controller import network_bp
    from controllers.notification_controller import notification_bp
    from controllers.profile_controller import profile_bp
    from controllers.register_controller import register_bp
    from controllers.splash_page_controller import splash_bp 
    from controllers.post_controller import post_bp

    # Blueprint kayıt
    app.register_blueprint(home_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(splash_bp)
    app.register_blueprint(post_bp)

    # Ana route
    @app.route('/')
    def hello():
        return "Merhaba, Nginx + Gunicorn ile çalışan Flask uygulaması!"

    @app.route('/lorem', methods=['POST'])
    def lorem():
        content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 2000
        return content

    # Görsel servisi
    @app.route('/images/<path:filename>')
    def serve_image(filename):
        return send_from_directory('images', filename)

    return app
