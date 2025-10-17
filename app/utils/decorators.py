"""Admin access control decorators for PSv2 Flask application.

This module provides decorators for controlling access to admin-only routes
and functionality. Uses Flask-Login's current_user to check role permissions.
"""

from functools import wraps
from flask import abort, flash, redirect, url_for, request
from flask_login import current_user


def admin_required(f):
    """Decorator to restrict access to admin users only.
    
    This decorator checks if the current user is authenticated and has
    role='admin'. If not, it redirects to login or shows a 403 error.
    
    Usage:
        @admin_required
        def admin_dashboard():
            return render_template('admin/dashboard.html')
    
    Returns:
        - 403 Forbidden if user is authenticated but not admin
        - Redirects to login if user is not authenticated
        - Allows access if user is authenticated admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('Please log in to access the admin area.', 'error')
            # Redirect to login with next parameter to return here after login
            return redirect(url_for('auth_bp.login', next=request.url))
        
        # Check if user has admin role
        if current_user.role != 'admin':
            flash('Access denied. This area requires administrator privileges. You are currently logged in as a customer.', 'error')
            # Redirect to home page instead of trying to render error template
            return redirect(url_for('home_bp.index'))
        
        # User is authenticated and has admin role - allow access
        return f(*args, **kwargs)
    
    return decorated_function


def role_required(required_role):
    """Decorator factory to restrict access to users with specific roles.
    
    This is a more flexible decorator that can check for any role.
    
    Args:
        required_role (str): The role required to access the route
        
    Usage:
        @role_required('admin')
        def admin_function():
            pass
            
        @role_required('customer')
        def customer_function():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this area.', 'error')
                return redirect(url_for('auth_bp.login', next=request.url))
            
            if current_user.role != required_role:
                flash(f'Access denied. {required_role.title()} privileges required.', 'error')
                abort(403)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator