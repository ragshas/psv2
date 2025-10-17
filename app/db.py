"""Flask-SQLAlchemy database integration for PS Framework v2."""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# SQLAlchemy extension instance
db = SQLAlchemy()
migrate = Migrate()


def init_db(app) -> None:
    """Initialize SQLAlchemy with the Flask app and create tables."""
    db.init_app(app)
    with app.app_context():
        db.create_all()

