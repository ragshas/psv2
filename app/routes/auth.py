"""Authentication blueprint for user login, registration, and logout."""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.models import User
from app.db import db

# Create auth blueprint with URL prefix '/auth'
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route - GET displays form, POST processes registration."""
    
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home_bp.index'))
    
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            # Validate input
            if not username:
                flash('Username is required.', 'error')
                return render_template('auth/register.html')
            
            if not password:
                flash('Password is required.', 'error')
                return render_template('auth/register.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('auth/register.html')
            
            # Check if username already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('auth/register.html')
            
            # Create new user
            new_user = User(username=username)
            new_user.set_password(password)
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth_bp.login'))
            
        except Exception as e:
            # Rollback on error
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('auth/register.html')
    
    # GET request - display registration form
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route - GET displays form, POST processes authentication."""
    
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home_bp.index'))
    
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            remember_me = request.form.get('remember_me') == 'on'
            
            # Validate input
            if not username:
                flash('Username is required.', 'error')
                return render_template('auth/login.html')
            
            if not password:
                flash('Password is required.', 'error')
                return render_template('auth/login.html')
            
            # Find user in database
            user = User.query.filter_by(username=username).first()
            
            # Verify credentials
            if user and user.verify_password(password):
                # Login successful
                login_user(user, remember=remember_me)
                flash(f'Welcome back, {user.username}!', 'success')
                
                # Redirect to next page or home
                next_page = request.form.get('next') or request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('home_bp.index'))
            else:
                # Invalid credentials
                flash('Invalid username or password.', 'error')
                return render_template('auth/login.html')
                
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
            return render_template('auth/login.html')
    
    # GET request - display login form
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route - requires login, logs out user and redirects to home."""
    
    try:
        username = current_user.username
        logout_user()
        flash(f'You have been logged out successfully, {username}.', 'info')
        
    except Exception as e:
        flash('An error occurred during logout.', 'error')
    
    return redirect(url_for('home_bp.index'))


# Additional utility routes for user management

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page - requires login."""
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password route - requires login."""
    
    if request.method == 'POST':
        try:
            # Get form data
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validate input
            if not current_password:
                flash('Current password is required.', 'error')
                return render_template('auth/change_password.html')
            
            if not new_password:
                flash('New password is required.', 'error')
                return render_template('auth/change_password.html')
            
            if len(new_password) < 6:
                flash('New password must be at least 6 characters long.', 'error')
                return render_template('auth/change_password.html')
            
            if new_password != confirm_password:
                flash('New passwords do not match.', 'error')
                return render_template('auth/change_password.html')
            
            # Verify current password
            if not current_user.verify_password(current_password):
                flash('Current password is incorrect.', 'error')
                return render_template('auth/change_password.html')
            
            # Update password
            current_user.set_password(new_password)
            db.session.commit()
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth_bp.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while changing password. Please try again.', 'error')
            return render_template('auth/change_password.html')
    
    # GET request - display change password form
    return render_template('auth/change_password.html')
