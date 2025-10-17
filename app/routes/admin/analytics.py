"""Admin analytics blueprint for PS Framework v2.

This module handles admin functionality for viewing analytics and business insights
including customer metrics, performance analytics, and business reporting.
"""

from flask import Blueprint, render_template
from app.utils.decorators import admin_required

# Create admin analytics blueprint with URL prefix
admin_analytics_bp = Blueprint('admin_analytics', __name__, url_prefix='/admin/analytics')


@admin_analytics_bp.route('/')
@admin_required
def analytics_dashboard():
    """Analytics and business insights dashboard.
    
    Renders the main analytics page where administrators can view
    business insights, customer metrics, and performance analytics.
    Accessible at /admin/analytics route.
    """
    return render_template('admin/analytics.html')