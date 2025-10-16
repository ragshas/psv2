"""Services blueprint for PS Framework v2.

Handles the services listing page where users can view all available services.
"""

from flask import Blueprint, render_template

from app.models import Service

# Create services blueprint
services_bp = Blueprint('services', __name__)


@services_bp.route('/services')
def services_list():
    """Display all services stored in the database.
    
    Fetches all services using Service.query.all() and renders them
    in the services.html template.
    """
    services = Service.query.all()
    return render_template('services.html', services=services)