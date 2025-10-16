# PSv2 Flask Application - AI Coding Instructions

## Project Overview

PSv2 is a **reusable Flask framework for small business websites** (pet shops, cake stores, etc.). It provides a complete solution with public website, user authentication, and admin dashboard that can be easily deployed and customized for different clients.

### Core Features
- **Public Website**: Home, services, shop, contact pages
- **User Authentication**: Login/register system using Flask-Login
- **Admin Dashboard**: Manage services and users
- **Database**: SQLite (`ps.db` stored in `/instance` directory)
- **Deployment**: Dockerized and GitHub-ready

### Key Architecture Patterns
- **App Factory Pattern**: Flask app created in `app/__init__.py` using `create_app()` function
- **Blueprint Organization**: Self-contained blueprints in `app/routes/` (home, auth, admin)
- **Template Hierarchy**: All templates extend `app/templates/base.html` using Jinja2
- **Instance Folder**: SQLite database and sensitive config in `instance/` directory

## Development Workflow

### Local Development
```bash
# Run with Docker (recommended)
docker-compose up

# Or run locally after setting up venv
pip install -r requirements.txt
python run.py
```

### Key Files & Responsibilities
- `run.py`: Application entry point - imports and runs Flask app from `app/__init__.py`
- `app/__init__.py`: App factory with Flask app creation, blueprint registration, and Flask-Login setup
- `app/models.py`: User model and database helpers for SQLite operations
- `instance/ps.db`: SQLite database file (auto-created)
- `docker-compose.yml`: Development environment with hot reload (volume mounted)

## Coding Conventions

### Route Organization
- Each route module in `app/routes/` should be a self-contained Flask Blueprint
- **Home Blueprint**: Public pages (home, services, shop, contact)
- **Auth Blueprint**: User login/register using Flask-Login
- **Admin Blueprint**: Dashboard for managing services and users
- Route files follow: `from flask import Blueprint; bp = Blueprint('name', __name__)`
- Register blueprints in `app/__init__.py` using `app.register_blueprint()`

### Template Structure
- All templates extend `app/templates/base.html` using Jinja2
- Use subdirectories for logical grouping (`auth/`, `admin/`)
- Design should be business-friendly and easily customizable for different clients

### Database Patterns
- SQLite database (`ps.db`) stored in `instance/` directory
- User model defined in `app/models.py` with Flask-Login integration
- Database helpers and initialization in `app/models.py`
- No separate `app/db.py` file needed for this simple setup

### Environment & Configuration
- Development runs on port 5000 (configured in docker-compose.yml)
- Use environment variables for sensitive configuration
- Store instance-specific config in `instance/` directory

## Docker Integration
- Base image: `python:3.11-slim`
- Application runs on port 5000 inside container
- Development mode uses volume mounting for live code changes
- `.dockerignore` excludes venv, git, and Docker files from build context

## Common Tasks
- **Add new route**: Create blueprint in `app/routes/`, register in `app/__init__.py`
- **Add database model**: Define in `app/models.py`, import in relevant route files
- **Add template**: Create in appropriate `app/templates/` subdirectory, extend base.html
- **Install dependencies**: Add to `requirements.txt`, rebuild Docker image
- **Customize for client**: Modify templates and static assets while keeping core logic intact

## Important Notes
- This project follows Flask best practices with blueprints and app factory pattern
- Keep blueprints self-contained to avoid duplicate imports
- Use Flask-Login for all authentication functionality
- Design templates to be easily customizable for different business types
- SQLite database automatically created in `instance/` directory
- Docker Compose is configured for development with live reload