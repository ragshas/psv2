"""Authentication helper functions and decorators for Flask routes."""

from functools import wraps
from flask import request, redirect, url_for, abort
from flask_login import current_user


def admin_required(view):
    """
    Decorator that restricts access to admin users only.
    
    Redirects unauthenticated users to login page.
    Returns 403 Forbidden for authenticated non-admin users.
    """
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth_bp.login', next=request.path))
        
        if current_user.role != 'admin':
            abort(403)
        
        return view(*args, **kwargs)
    
    return wrapped_view