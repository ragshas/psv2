# 🧭 COPILOT INSTRUCTION:
# Create a Flask application for PS Framework v2.
# The file should import create_app() from app/__init__.py,
# call it to create the Flask app, and run it in debug mode.
# Use `if __name__ == "__main__":` to start the app.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


        