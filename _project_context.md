# 🧭 PS Framework v2 — Project Context

Goal:
- Build a clean, modular Flask web application for small businesses (e.g. pet shop, cake store, etc.).
- Should be portable (Dockerized) and reusable for multiple clients.
- Core features:
  - Public website (home, services, shop, contact)
  - User authentication (login/register)
  - Admin dashboard (manage services and users)
- Database: SQLite (ps.db in /instance)
- Architecture:
  - app/__init__.py → creates Flask app
  - app/models.py → defines User model and DB helpers
  - app/routes → each blueprint (home, auth, admin)
  - app/templates → all HTML templates
  - Docker + GitHub ready for deployment
- Copilot should:
  - Keep each blueprint self-contained (no duplicate imports)
  - Suggest code consistent with this architecture
  - Use Flask-Login for authentication
  - Use Jinja2 templates with base.html
