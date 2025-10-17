from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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


class Booking(db.Model):
    """Booking model linking users to services. Supports both registered users and guest bookings."""
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for guest bookings
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    notes = db.Column(db.Text)
    
    # Guest booking fields (used when user_id is None)
    guest_name = db.Column(db.String(100))
    guest_email = db.Column(db.String(120))
    guest_phone = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    service = db.relationship('Service', backref=db.backref('bookings', lazy=True))
    
    def get_customer_name(self):
        """Get the customer name for display (either registered user or guest)."""
        return self.user.username if self.user else self.guest_name
    
    def get_customer_email(self):
        """Get the customer email (either registered user or guest)."""
        # Note: User model doesn't have email field currently, so we'd use guest_email or None
        return self.guest_email
    
    def is_guest_booking(self):
        """Check if this is a guest booking."""
        return self.user_id is None
    
    def __repr__(self):
        customer_name = self.get_customer_name()
        return f'<Booking {customer_name} - {self.service.name}>'


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

