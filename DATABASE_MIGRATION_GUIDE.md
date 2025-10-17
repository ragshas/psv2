# Database Migration Guide for PSv2

## Overview
PSv2 now uses Flask-Migrate to handle database schema changes safely without losing user data. This is essential for production deployments where you need to modify database tables without clearing existing records.

## Initial Setup (First Time Only)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize migration repository:**
   ```bash
   flask db init
   ```
   This creates a `migrations/` folder to track all database changes.

3. **Create initial migration for existing models:**
   ```bash
   flask db migrate -m "Initial migration with User and Service models"
   ```
   This scans your models and creates the first migration file.

4. **Apply the migration:**
   ```bash
   flask db upgrade
   ```
   This creates the database tables based on your models.

## Adding/Modifying Database Columns

### When you want to add a new column (like we did with `created_at`):

1. **Modify your model in `app/models.py`:**
   ```python
   class User(UserMixin, db.Model):
       # ... existing fields ...
       created_at = db.Column(db.DateTime, default=datetime.utcnow)  # New field
   ```

2. **Generate migration:**
   ```bash
   flask db migrate -m "Add created_at field to User model"
   ```
   Flask-Migrate detects the change and creates a migration file.

3. **Review the migration file:**
   Check `migrations/versions/xxxx_add_created_at_field.py` to ensure it looks correct.

4. **Apply the migration:**
   ```bash
   flask db upgrade
   ```
   This safely adds the new column without losing existing user data.

### When you want to remove a column:

1. **Remove from model:**
   Delete the field from your model class.

2. **Generate migration:**
   ```bash
   flask db migrate -m "Remove old_column from User model"
   ```

3. **Apply migration:**
   ```bash
   flask db upgrade
   ```

## Development vs Production

### Development Environment:
- Use Docker Compose with volume mounting for live changes
- Run migrations inside the container:
  ```bash
  docker-compose exec web flask db migrate -m "Your message"
  docker-compose exec web flask db upgrade
  ```

### Production Environment:
- Always backup your database before applying migrations
- Test migrations on a copy of production data first
- Apply migrations during maintenance windows:
  ```bash
  flask db upgrade
  ```

## Common Migration Commands

```bash
# Initialize migration repository (first time only)
flask db init

# Create a new migration after model changes
flask db migrate -m "Description of changes"

# Apply pending migrations
flask db upgrade

# Show migration history
flask db history

# Downgrade to previous migration (be careful!)
flask db downgrade

# Show current migration version
flask db current
```

## Important Notes

1. **Never edit migration files manually** unless you know what you're doing
2. **Always review generated migrations** before applying them
3. **Backup production databases** before running migrations
4. **Test migrations on development/staging** before production
5. **The `migrations/` folder should be committed to git** to track schema changes

## Current Status

With Flask-Migrate now fully integrated:
- ✅ Flask-Migrate added to requirements.txt 
- ✅ Migration system initialized in `app/__init__.py`
- ✅ Migrations folder created with `flask db init`
- ✅ Initial migration created for current models with `created_at` field
- ✅ Database schema is now under version control
- ✅ Custom CLI commands moved to `flask database` to avoid conflicts

## Next Steps

Your database is now properly managed with Flask-Migrate! When you want to add/modify fields:

1. **Modify your model** in `app/models.py`
2. **Generate migration:** `flask db migrate -m "Description"`  
3. **Review migration file** in `migrations/versions/`
4. **Apply migration:** `flask db upgrade`

## Important SQLite Notes

- SQLite has limited ALTER TABLE support
- When adding unique constraints, provide explicit names:
  ```python
  email = db.Column(db.String(120), nullable=True)
  # Add unique constraint separately if needed
  __table_args__ = (db.UniqueConstraint('email', name='uq_user_email'),)
  ```
- Complex schema changes may require manual migration editing
- Always test migrations on development data first

## Production Deployment

1. **Backup your database** before any migration
2. **Test on staging** with production data copy  
3. **Apply migrations** during maintenance window
4. **Monitor** application after deployment