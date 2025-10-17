"""Admin bookings management blueprint for PS Framework v2.

This module handles admin functionality for managing bookings and orders including
viewing customer bookings, managing scheduling, and handling order fulfillment.
"""

from flask import Blueprint, redirect, url_for
from app.utils.decorators import admin_required

# Create admin bookings blueprint with URL prefix
admin_bookings_bp = Blueprint('admin_bookings', __name__, url_prefix='/admin/bookings')


@admin_bookings_bp.route('/')
@admin_required
def bookings_dashboard():
    """Bookings and orders management dashboard.
    
    Redirects to the main bookings page where administrators can view all
    customer bookings and manage their status.
    Accessible at /admin/bookings route.
    """
    return redirect(url_for('bookings.all_bookings'))