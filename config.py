"""
Конфигурация Flask приложения
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Базовая конфигурация."""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hermitage.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PostgreSQL Schema (для изоляции проектов в одной БД)
    DATABASE_SCHEMA = os.environ.get('DATABASE_SCHEMA', 'hermitage')
    
    # Настройка schema для SQLAlchemy (PostgreSQL)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgresql'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {
                'options': f'-c search_path={DATABASE_SCHEMA},public'
            }
        }
    
    # OpenAI
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Mail (для контактной формы)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.strato.de')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'info@hermitage-frankfurt.de')
    
    # Контактный email для получения заявок
    CONTACT_EMAIL = 'info@hermitage-frankfurt.de'
    
    # Chatbot
    CHATBOT_MODEL = os.environ.get('CHATBOT_MODEL', 'gpt-4o-mini')
    CHATBOT_MAX_TOKENS = 500
    
    # Blog
    BLOG_POSTS_PER_PAGE = 10
    AUTO_BLOG_ENABLED = True
    MAX_BLOG_ARTICLES = int(os.environ.get('MAX_BLOG_ARTICLES', 30))


class DevelopmentConfig(Config):
    """Конфигурация для разработки."""
    DEBUG = True


class ProductionConfig(Config):
    """Конфигурация для продакшена."""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
