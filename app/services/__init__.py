"""
Инициализация сервисов
"""

from app.services.chatbot import ChatbotService
from app.services.blog_generator import BlogGenerator, ContentScheduler
from app.services.trends_fetcher import TrendsFetcher

__all__ = ['ChatbotService', 'BlogGenerator', 'ContentScheduler', 'TrendsFetcher']
