"""Booking management routes for PSv2."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.db import db
from app.models import Booking, Service, User

# Create bookings blueprint
bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')


@bookings_bp.route('/new/<int:service_id>', methods=['GET', 'POST'])
def new_booking(service_id):
    """Create a new booking for a service."""
    # Get the service or return 404
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        # Get form data
        booking_date_str = request.form.get('booking_date')
        booking_time_str = request.form.get('booking_time')
        notes = request.form.get('notes', '').strip()
        
        # Guest booking fields
        guest_name = request.form.get('guest_name', '').strip()
        guest_email = request.form.get('guest_email', '').strip()
        guest_phone = request.form.get('guest_phone', '').strip()
        
        # Validate required fields
        if not booking_date_str or not booking_time_str:
            flash('Booking date and time are required.', 'error')
            return render_template('bookings/new.html', service=service)
        
        # For guest bookings, validate required guest fields
        if not current_user.is_authenticated:
            if not guest_name or not guest_email:
                flash('Name and email are required for booking.', 'error')
                return render_template('bookings/new.html', service=service)
        
        try:
            # Combine date and time into datetime object
            booking_datetime_str = f"{booking_date_str} {booking_time_str}"
            booking_datetime = datetime.strptime(booking_datetime_str, '%Y-%m-%d %H:%M')
            
            # Check if booking date is in the future
            if booking_datetime <= datetime.now():
                flash('Booking date must be in the future.', 'error')
                return render_template('bookings/new.html', service=service)
            
            # Create new booking
            if current_user.is_authenticated:
                # Registered user booking
                booking = Booking(
                    user_id=current_user.id,
                    service_id=service_id,
                    booking_date=booking_datetime,
                    notes=notes,
                    status='pending'
                )
            else:
                # Guest booking
                booking = Booking(
                    user_id=None,
                    service_id=service_id,
                    booking_date=booking_datetime,
                    notes=notes,
                    guest_name=guest_name,
                    guest_email=guest_email,
                    guest_phone=guest_phone,
                    status='pending'
                )
            
            db.session.add(booking)
            db.session.commit()
            
            customer_name = current_user.username if current_user.is_authenticated else guest_name
            flash(f'Booking created successfully for {service.name}, {customer_name}!', 'success')
            
            # Redirect based on user type
            if current_user.is_authenticated:
                return redirect(url_for('bookings.all_bookings'))
            else:
                # For guests, redirect to services page with confirmation
                return redirect(url_for('services.services_list'))
            
        except ValueError:
            flash('Invalid date or time format.', 'error')
            return render_template('bookings/new.html', service=service)
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the booking. Please try again.', 'error')
            return render_template('bookings/new.html', service=service)
    
    # GET request - show booking form
    from datetime import date, timedelta
    tomorrow = date.today() + timedelta(days=1)
    min_date = tomorrow.strftime('%Y-%m-%d')
    return render_template('bookings/new.html', service=service, min_date=min_date)


@bookings_bp.route('/all')
@login_required
def all_bookings():
    """List bookings based on user role."""
    if current_user.role == 'admin':
        # Admins see all bookings
        bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
        page_title = "All Bookings"
    else:
        # Customers see only their own bookings
        bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
        page_title = "My Bookings"
    
    return render_template('bookings/all.html', bookings=bookings, page_title=page_title)


@bookings_bp.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking (customers can cancel their own, admins can cancel any)."""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check permissions - only registered users can cancel through this route
    # Guest bookings would need to contact business directly
    if current_user.role != 'admin' and booking.user_id != current_user.id:
        abort(403)  # Forbidden
    
    # Check if booking can be cancelled
    if booking.status in ['cancelled', 'completed']:
        flash('This booking cannot be cancelled.', 'error')
        return redirect(url_for('bookings.all_bookings'))
    
    # Cancel the booking
    booking.status = 'cancelled'
    booking.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash('Booking cancelled successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while cancelling the booking.', 'error')
    
    return redirect(url_for('bookings.all_bookings'))


@bookings_bp.route('/update-status/<int:booking_id>', methods=['POST'])
@login_required
def update_status(booking_id):
    """Update booking status (admin only)."""
    if current_user.role != 'admin':
        abort(403)  # Only admins can update booking status
    
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    
    # Validate status
    valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
    if new_status not in valid_statuses:
        flash('Invalid status selected.', 'error')
        return redirect(url_for('bookings.all_bookings'))
    
    # Update status
    booking.status = new_status
    booking.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash(f'Booking status updated to {new_status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the booking status.', 'error')
    
    return redirect(url_for('bookings.all_bookings'))