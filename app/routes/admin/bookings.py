"""Admin bookings management blueprint for PS Framework v2.

This module handles admin functionality for managing bookings and orders including
viewing customer bookings, managing scheduling, and handling order fulfillment.
"""

from flask import Blueprint, render_template

# Create admin bookings blueprint with URL prefix
admin_bookings_bp = Blueprint('admin_bookings', __name__, url_prefix='/admin/bookings')


@admin_bookings_bp.route('/')
def bookings_dashboard():
    """Bookings and orders management dashboard.
    
    Renders the main bookings management page where administrators can view
    customer bookings, manage scheduling, and handle order fulfillment.
    Accessible at /admin/bookings route.
    """
    return render_template('admin/bookings.html')