"""Contact blueprint for contact form and inquiries."""

from flask import Blueprint, render_template, request, flash, redirect, url_for
import re

# Create contact blueprint
contact_bp = Blueprint('contact_bp', __name__)


@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form for customer inquiries."""
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()
            
            # Validate name
            if not name:
                flash('Name is required.', 'error')
                return render_template('contact.html')
            
            if len(name) < 2:
                flash('Name must be at least 2 characters long.', 'error')
                return render_template('contact.html')
            
            # Validate email
            if not email:
                flash('Email is required.', 'error')
                return render_template('contact.html')
            
            # Simple email validation regex
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                flash('Please enter a valid email address.', 'error')
                return render_template('contact.html')
            
            # Validate message
            if not message:
                flash('Message is required.', 'error')
                return render_template('contact.html')
            
            if len(message) < 10:
                flash('Message must be at least 10 characters long.', 'error')
                return render_template('contact.html')
            
            # If all validation passes
            flash(f'Thank you, {name}! Your message has been sent successfully. We will get back to you soon.', 'success')
            return redirect(url_for('contact_bp.contact'))
            
        except Exception as e:
            flash('An error occurred while sending your message. Please try again.', 'error')
            return render_template('contact.html')
    
    # GET request - display contact form
    return render_template('contact.html')