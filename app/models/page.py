"""
Модель для статических страниц сайта
"""

from datetime import datetime
from app import db


class Page(db.Model):
    """Статические страницы сайта (Fliesen, Innenausstattung, etc.)."""
    
    __tablename__ = 'pages'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text)
    
    # SEO
    seo_title = db.Column(db.String(255))
    seo_description = db.Column(db.String(500))
    
    # Медиа
    hero_image = db.Column(db.String(500))
    images = db.Column(db.JSON)  # Список изображений для галереи
    
    # FAQ (для аккордеона)
    faq = db.Column(db.JSON)  # [{"question": "...", "answer": "..."}]
    
    # Мета
    template = db.Column(db.String(100), default='default')
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Page {self.slug}>'
    
    def get_seo_title(self):
        """Возвращает SEO заголовок или обычный заголовок."""
        return self.seo_title or f'{self.title} | Hermitage Frankfurt'
    
    def get_seo_description(self):
        """Возвращает SEO описание или первые 160 символов контента."""
        if self.seo_description:
            return self.seo_description
        if self.content:
            return self.content[:160].strip() + '...'
        return 'Hermitage Frankfurt - Ihr Experte für Fliesen und Innenausstattung'
