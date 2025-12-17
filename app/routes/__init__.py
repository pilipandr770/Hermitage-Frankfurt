"""
Инициализация маршрутов
"""

from app.routes.main import main_bp
from app.routes.blog import blog_bp
from app.routes.api import api_bp
from app.routes.admin import admin_bp

__all__ = ['main_bp', 'blog_bp', 'api_bp', 'admin_bp']
