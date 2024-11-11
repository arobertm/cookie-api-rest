from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)

    # Înregistrăm blueprints
    from app.auth.routes import auth_bp
    from app.v1.routes import v1_bp
    from app.v2.routes import v2_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(v1_bp, url_prefix='/api/v1')
    app.register_blueprint(v2_bp, url_prefix='/api/v2')

    return app