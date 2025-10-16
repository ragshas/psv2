import os
from flask import Flask, app
from app.db import db

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

    # ---- Import Models ----
    from app import models  # Must import models before creating tables

    # ---- Auto-create Tables ----
    with app.app_context():
        db.create_all()
        print("✅ Database initialized and tables created (if not existing).")

    # ---- Register Blueprints ----
    from app.routes.home import home_bp
    app.register_blueprint(home_bp)
    from app.routes.services import services_bp
    app.register_blueprint(services_bp)
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
