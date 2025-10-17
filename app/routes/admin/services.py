"""Admin services management blueprint for PS Framework v2.

This module handles admin functionality for managing services including
adding new services, editing existing ones, and handling service data.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort

from app.models import Service
from app.db import db
from app.utils.decorators import admin_required

# Create admin services blueprint with URL prefix
admin_services_bp = Blueprint('admin_services', __name__, url_prefix='/admin/services')


@admin_services_bp.route('/')
@admin_required
def services_management():
    """Admin services management homepage.
    
    Renders the services management page where administrators can view all
    services, add new ones, edit existing services, and manage service data.
    Accessible at /admin/services route.
    """
    services = Service.query.all()
    return render_template('admin/services_management.html', services=services)


@admin_services_bp.route('/new', methods=['GET'])
@admin_required
def new_service():
    """Show form for adding a new service.
    
    Renders the add service form template for administrators to input
    service details like name, description, and price.
    """
    return render_template('admin/add_service.html')


@admin_services_bp.route('/new', methods=['POST'])
@admin_required
def create_service():
    """Handle form submission to create a new service.
    
    Processes the form data from the add service form, validates the input,
    saves the new service to the database, and redirects back to admin dashboard.
    Shows flash messages for success or error feedback.
    """
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_str = request.form.get('price', '').strip()
        
        # Validate required fields
        if not name:
            flash('Service name is required.', 'error')
            return render_template('admin/add_service.html')
        
        # Convert price to float if provided
        price = None
        if price_str:
            try:
                price = float(price_str)
                if price < 0:
                    flash('Price must be a positive number.', 'error')
                    return render_template('admin/add_service.html')
            except ValueError:
                flash('Price must be a valid number.', 'error')
                return render_template('admin/add_service.html')
        
        # Create new service
        new_service = Service(
            name=name,
            description=description if description else None,
            price=price
        )
        
        # Save to database
        db.session.add(new_service)
        db.session.commit()
        
        flash(f'Service "{name}" has been added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        flash('An error occurred while adding the service. Please try again.', 'error')
        return render_template('admin/add_service.html')


@admin_services_bp.route('/edit/<int:id>', methods=['GET'])
@admin_required
def edit_service(id):
    """Show form for editing an existing service.
    
    Renders the edit service form template pre-filled with existing service data.
    Returns 404 if service with given ID doesn't exist.
    """
    service = Service.query.get_or_404(id)
    return render_template('admin/edit_service.html', service=service)


@admin_services_bp.route('/edit/<int:id>', methods=['POST'])
@admin_required
def update_service(id):
    """Handle form submission to update an existing service.
    
    Processes the form data from the edit service form, validates the input,
    updates the service in the database, and redirects back to services management.
    Shows flash messages for success or error feedback.
    """
    service = Service.query.get_or_404(id)
    
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_str = request.form.get('price', '').strip()
        
        # Validate required fields
        if not name:
            flash('Service name is required.', 'error')
            return render_template('admin/edit_service.html', service=service)
        
        # Convert price to float if provided
        price = None
        if price_str:
            try:
                price = float(price_str)
                if price < 0:
                    flash('Price must be a positive number.', 'error')
                    return render_template('admin/edit_service.html', service=service)
            except ValueError:
                flash('Price must be a valid number.', 'error')
                return render_template('admin/edit_service.html', service=service)
        
        # Update service
        service.name = name
        service.description = description if description else None
        service.price = price
        
        # Save to database
        db.session.commit()
        
        flash(f'Service "{name}" has been updated successfully!', 'success')
        return redirect(url_for('admin_services.services_management'))
        
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        flash('An error occurred while updating the service. Please try again.', 'error')
        return render_template('admin/edit_service.html', service=service)


@admin_services_bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_service(id):
    """Handle deletion of an existing service.
    
    Deletes the service from the database and redirects back to services management.
    Shows flash message confirming deletion. Returns 404 if service doesn't exist.
    """
    service = Service.query.get_or_404(id)
    service_name = service.name  # Store name for flash message before deletion
    
    try:
        # Delete service from database
        db.session.delete(service)
        db.session.commit()
        
        flash(f'Service "{service_name}" has been deleted successfully!', 'success')
        
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        flash('An error occurred while deleting the service. Please try again.', 'error')
    
    return redirect(url_for('admin_services.services_management'))