from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """User model for authentication and user management."""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        """Verify the user's password against the stored hash."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Service(db.Model):
    """Service model for business services."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Service {self.name}>'


# Helper methods
def add_user(username, password, role='customer'):
    """Create and add a new user to the database."""
    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def add_service(name, description=None, price=None):
    """Create and add a new service to the database."""
    service = Service(name=name, description=description, price=price)
    db.session.add(service)
    db.session.commit()
    return service


def get_all_services():
    """Return all services from the database."""
    return Service.query.all()

