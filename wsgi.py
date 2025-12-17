"""
WSGI entry point for Gunicorn on Render.com
"""
from app import create_app

# Create the Flask application instance
app = create_app('production')

# This allows running: gunicorn wsgi:app
if __name__ == "__main__":
    app.run()
