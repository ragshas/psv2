"""Flask CLI commands for administrative tasks."""

import click
from flask import current_app
from flask.cli import with_appcontext
from app.db import db
from app.models import User, Service


# User Management Commands

@click.group('user')
def user_cli():
    """User management commands."""
    pass


@user_cli.command('list')
@with_appcontext
def list_users():
    """List all users in the database."""
    users = User.query.all()
    
    if not users:
        click.echo(click.style('⚠️  No users found.', fg='yellow'))
        return
    
    # Print table header
    click.echo(click.style('ID | Username | Role', fg='cyan'))
    click.echo(click.style('---|----------|-----', fg='cyan'))
    
    # Print each user
    for user in users:
        role_color = 'yellow' if user.role == 'admin' else 'green'
        click.echo(click.style(f'{user.id:2} | {user.username:8} | {user.role}', fg=role_color))


@user_cli.command('create-admin')
@with_appcontext
def create_admin():
    """Create a new admin user."""
    click.echo(click.style('Creating admin user...', fg='blue'))
    
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    
    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        click.echo(click.style(f'⚠️  User "{username}" already exists!', fg='yellow'))
        return
    
    # Create new admin user
    admin_user = User(username=username, role='admin')
    admin_user.set_password(password)
    
    db.session.add(admin_user)
    db.session.commit()
    
    click.echo(click.style(f'✅ Admin user "{username}" created successfully.', fg='green'))


@user_cli.command('edit-role')
@with_appcontext
def edit_user_role():
    """Edit a user's role in the database."""
    username = click.prompt('Username')
    new_role = click.prompt('New role')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(click.style('⚠️  User not found.', fg='yellow'))
        return
    
    old_role = user.role
    user.role = new_role
    db.session.commit()
    
    click.echo(click.style(f'✅ User "{username}" role changed from "{old_role}" to "{new_role}".', fg='green'))


@user_cli.command('delete')
@with_appcontext
def delete_user():
    """Delete a user from the database."""
    username = click.prompt('Username to delete')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(click.style('⚠️  User not found.', fg='yellow'))
        return
    
    if not click.confirm(f'Are you sure you want to delete user "{username}"?'):
        click.echo(click.style('User deletion cancelled.', fg='yellow'))
        return
    
    db.session.delete(user)
    db.session.commit()
    
    click.echo(click.style(f'🗑️  User "{username}" deleted successfully.', fg='green'))


# Service Management Commands

@click.group('service')
def service_cli():
    """Service management commands."""
    pass


@service_cli.command('list')
@with_appcontext
def list_services():
    """List all services in the database."""
    services = Service.query.all()
    
    if not services:
        click.echo(click.style('⚠️  No services found.', fg='yellow'))
        return
    
    # Print table header
    click.echo(click.style('ID | Name                 | Description                    | Price', fg='cyan'))
    click.echo(click.style('---|----------------------|--------------------------------|--------', fg='cyan'))
    
    # Print each service
    for service in services:
        name = (service.name[:20] + '...') if len(service.name) > 20 else service.name
        desc = (service.description[:30] + '...') if service.description and len(service.description) > 30 else (service.description or '')
        price = f'${service.price:.2f}' if service.price else 'N/A'
        click.echo(click.style(f'{service.id:2} | {name:20} | {desc:30} | {price:>7}', fg='green'))


@service_cli.command('add')
@with_appcontext
def add_service():
    """Add a new service to the database."""
    click.echo(click.style('Adding new service...', fg='blue'))
    
    name = click.prompt('Service name')
    description = click.prompt('Description', default='')
    price_input = click.prompt('Price', default='')
    
    # Check if service already exists
    existing_service = Service.query.filter_by(name=name).first()
    if existing_service:
        click.echo(click.style(f'⚠️  Service "{name}" already exists!', fg='yellow'))
        return
    
    # Parse price
    price = None
    if price_input:
        try:
            price = float(price_input)
        except ValueError:
            click.echo(click.style('⚠️  Invalid price format. Service created without price.', fg='yellow'))
    
    # Create new service
    new_service = Service(name=name, description=description or None, price=price)
    
    db.session.add(new_service)
    db.session.commit()
    
    click.echo(click.style(f'✅ Service "{name}" created successfully.', fg='green'))


@service_cli.command('edit')
@with_appcontext
def edit_service():
    """Edit a service in the database."""
    service_input = click.prompt('Service ID or name to edit')
    
    # Try to find by ID first, then by name
    service = None
    if service_input.isdigit():
        service = Service.query.get(int(service_input))
    if not service:
        service = Service.query.filter_by(name=service_input).first()
    
    if not service:
        click.echo(click.style('⚠️  Service not found.', fg='yellow'))
        return
    
    click.echo(click.style(f'Editing service: {service.name}', fg='blue'))
    click.echo(click.style('Leave fields blank to keep current values.', fg='blue'))
    
    # Get new values
    new_name = click.prompt(f'Name [{service.name}]', default='', show_default=False)
    new_desc = click.prompt(f'Description [{service.description or "None"}]', default='', show_default=False)
    new_price = click.prompt(f'Price [{service.price or "None"}]', default='', show_default=False)
    
    # Update fields if new values provided
    if new_name:
        service.name = new_name
    if new_desc:
        service.description = new_desc
    if new_price:
        try:
            service.price = float(new_price)
        except ValueError:
            click.echo(click.style('⚠️  Invalid price format. Price not updated.', fg='yellow'))
    
    db.session.commit()
    click.echo(click.style(f'✏️  Service "{service.name}" updated successfully.', fg='green'))


@service_cli.command('delete')
@with_appcontext
def delete_service():
    """Delete a service from the database."""
    service_input = click.prompt('Service ID or name to delete')
    
    # Try to find by ID first, then by name
    service = None
    if service_input.isdigit():
        service = Service.query.get(int(service_input))
    if not service:
        service = Service.query.filter_by(name=service_input).first()
    
    if not service:
        click.echo(click.style('⚠️  Service not found.', fg='yellow'))
        return
    
    if not click.confirm(f'Are you sure you want to delete service "{service.name}"?'):
        click.echo(click.style('Service deletion cancelled.', fg='yellow'))
        return
    
    service_name = service.name
    db.session.delete(service)
    db.session.commit()
    
    click.echo(click.style(f'🗑️  Service "{service_name}" deleted successfully.', fg='green'))


# Database Management Commands

@click.group('db')
def db_cli():
    """Database management commands."""
    pass


@db_cli.command('reset')
@with_appcontext
def reset_db():
    """Reset the database by dropping and recreating all tables."""
    click.echo(click.style('⚠️  This will delete ALL data in the database!', fg='red'))
    
    if not click.confirm('Are you sure you want to reset the database?'):
        click.echo(click.style('Database reset cancelled.', fg='yellow'))
        return
    
    # Drop all tables and recreate
    db.drop_all()
    db.create_all()
    
    click.echo(click.style('✅ Database reset successfully!', fg='green'))


@db_cli.command('status')
@with_appcontext
def db_status():
    """Show database status with counts of users and services."""
    user_count = User.query.count()
    service_count = Service.query.count()
    
    click.echo(click.style('📊 Database Status', fg='cyan'))
    click.echo(click.style('----------------', fg='cyan'))
    click.echo(click.style(f'👥 Users: {user_count}', fg='green'))
    click.echo(click.style(f'🛠️  Services: {service_count}', fg='green'))


def register_commands(app):
    """Register CLI commands with the Flask app."""
    app.cli.add_command(user_cli)
    app.cli.add_command(service_cli)
    app.cli.add_command(db_cli)