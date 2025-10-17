"""Customer Account management blueprint for PS Framework v2.

This module handles customer account functionality including profile viewing,
account management, and customer-specific features. Provides a dedicated
interface for logged-in customers to manage their account information.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

# Create account blueprint
account_bp = Blueprint('account', __name__, url_prefix='/account')


@account_bp.route('/')
@login_required
def profile():
    """Customer account profile page.
    
    Shows the user's profile information including username, role, and join date.
    Accessible at /account route for logged-in users only.
    
    Admin users are automatically redirected to the admin dashboard since they
    have their own dedicated admin interface.
    """
    # Redirect admin users to their dashboard
    if current_user.role == 'admin':
        flash('Admin users should use the Admin Dashboard for account management.', 'info')
        return redirect(url_for('admin.dashboard'))
    
    # Calculate days as member
    days_as_member = 0
    if current_user.created_at:
        days_as_member = (datetime.utcnow() - current_user.created_at).days
    
    # Show customer profile page
    return render_template('account/profile.html', user=current_user, days_as_member=days_as_member)


@account_bp.route('/settings')
@login_required
def settings():
    """Account settings page (placeholder for future development).
    
    This route is prepared for future account settings functionality
    like password changes, preferences, etc.
    """
    # Redirect admin users to their dashboard
    if current_user.role == 'admin':
        flash('Admin users should use the Admin Dashboard for account management.', 'info')
        return redirect(url_for('admin.dashboard'))
    
    # Placeholder for account settings
    flash('Account settings coming soon!', 'info')
    return redirect(url_for('account.profile'))