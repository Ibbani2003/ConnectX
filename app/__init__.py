import os
from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    
    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.communities import bp as communities_bp
    app.register_blueprint(communities_bp, url_prefix='/communities')
    
    from app.collaborations import bp as collaborations_bp
    app.register_blueprint(collaborations_bp, url_prefix='/collaborations')
    
    from app.messages import bp as messages_bp
    app.register_blueprint(messages_bp, url_prefix='/messages')

    from app.notifications import bp as notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/notifications')

    return app
