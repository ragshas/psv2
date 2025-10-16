"""Admin dashboard blueprint for PS Framework v2.

This module handles the admin dashboard for managing services, bookings,
and future administrative features. Provides a centralized interface
for business owners to manage their PS Framework application.
"""

from flask import Blueprint, render_template

# Create admin blueprint with URL prefix
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
def dashboard():
    """Admin dashboard homepage.
    
    Renders the main admin dashboard where administrators can access
    different management sections through summary cards.
    Accessible at /admin route.
    """
    return render_template('admin/dashboard.html')
