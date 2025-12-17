"""
Hermitage Frankfurt - Flask Application Factory
Витринный сайт для магазина плитки и интерьера
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config, Config

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name='development'):
    """Фабрика приложения Flask."""
    app = Flask(__name__)
    
    # Загрузка конфигурации по имени или объекту
    if isinstance(config_name, str):
        app.config.from_object(config.get(config_name, config['default']))
    else:
        app.config.from_object(config_name)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Настройка login manager
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Bitte melden Sie sich an.'
    login_manager.login_message_category = 'warning'

    # Регистрация blueprints
    from app.routes.main import main_bp
    from app.routes.blog import blog_bp
    from app.routes.api import api_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Исключаем API из CSRF проверки (для AJAX запросов чатбота)
    csrf.exempt(api_bp)

    # Создание таблиц
    with app.app_context():
        db.create_all()

    # Контекстные процессоры
    @app.context_processor
    def inject_globals():
        """Глобальные переменные для шаблонов."""
        import os
        return {
            'company_name': 'Hermitage Frankfurt',
            'company_phone': '069 90475570',
            'company_email': 'info@hermitage-frankfurt.de',
            'company_address': 'Hanauer Landstraße 421, 60314 Frankfurt am Main',
            'current_year': 2025,
            'config': {
                'OPENAI_API_KEY': bool(os.environ.get('OPENAI_API_KEY')),
                'NEWS_API_KEY': bool(os.environ.get('NEWS_API_KEY')),
            }
        }

    return app
