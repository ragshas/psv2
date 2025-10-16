"""Admin users management blueprint for PS Framework v2.

This module handles admin functionality for managing users including
viewing user accounts, managing roles, and handling user permissions.
"""

from flask import Blueprint, render_template

# Create admin users blueprint with URL prefix
admin_users_bp = Blueprint('admin_users', __name__, url_prefix='/admin/users')


@admin_users_bp.route('/')
def users_dashboard():
    """User management dashboard.
    
    Renders the main user management page where administrators can view
    and manage user accounts, roles, and permissions.
    Accessible at /admin/users route.
    """
    return render_template('admin/users.html')