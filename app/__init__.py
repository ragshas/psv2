import os
from flask import Flask, app
from flask_login import LoginManager
from app.db import db, migrate

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # ---- Basic Config ----
    app.config["SECRET_KEY"] = "dev"  # You can replace with a real secret in production
    os.makedirs(app.instance_path, exist_ok=True)

    # ---- Database Config ----
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, 'ps.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ---- Initialize SQLAlchemy ----
    db.init_app(app)

    # ---- Initialize Flask-Migrate ----
    migrate.init_app(app, db)

    # ---- Register custom CLI commands ----
    from app.cli import register_commands
    register_commands(app)

    # ---- Initialize Flask-Login ----
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # ---- Error Handlers ----
    @app.errorhandler(403)
    def access_denied(error):
        from flask import render_template
        return render_template('errors/403.html'), 403

    # ---- Import Models ----
    from app import models  # Must import models before creating tables

    # ---- Register Blueprints ----
    from app.routes.home import home_bp
    app.register_blueprint(home_bp)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.account import account_bp
    app.register_blueprint(account_bp)
    from app.routes.shop import shop_bp
    app.register_blueprint(shop_bp)
    from app.routes.contact import contact_bp
    app.register_blueprint(contact_bp)
    from app.routes.services import services_bp
    app.register_blueprint(services_bp)
    from app.routes.bookings import bookings_bp
    app.register_blueprint(bookings_bp)
    from app.routes.admin.dashboard import admin_bp
    app.register_blueprint(admin_bp)
    from app.routes.admin.services import admin_services_bp
    app.register_blueprint(admin_services_bp)
    from app.routes.admin.users import admin_users_bp
    app.register_blueprint(admin_users_bp)
    from app.routes.admin.bookings import admin_bookings_bp
    app.register_blueprint(admin_bookings_bp)
    from app.routes.admin.analytics import admin_analytics_bp
    app.register_blueprint(admin_analytics_bp)


    # (Later we'll add services, shop, auth blueprints here)
    
    return app
