"""
Модели для блога и контент-плана
"""

from datetime import datetime
from app import db


class BlogPost(db.Model):
    """Статьи блога."""
    
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    excerpt = db.Column(db.String(500))  # Краткое описание
    content = db.Column(db.Text, nullable=False)
    
    # Медиа
    featured_image = db.Column(db.String(500))
    
    # Категоризация
    category = db.Column(db.String(100), default='Trends')
    tags = db.Column(db.JSON)  # ["fliesen", "badezimmer", ...]
    
    # SEO
    seo_title = db.Column(db.String(255))
    seo_description = db.Column(db.String(500))
    
    # Статус публикации
    is_published = db.Column(db.Boolean, default=False)
    is_auto_generated = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    
    # Мета
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.slug}>'
    
    def publish(self):
        """Публикует статью."""
        self.is_published = True
        self.published_at = datetime.utcnow()
    
    def increment_views(self):
        """Увеличивает счётчик просмотров."""
        self.views_count += 1
    
    @staticmethod
    def get_published():
        """Возвращает опубликованные статьи."""
        return BlogPost.query.filter_by(is_published=True)\
            .order_by(BlogPost.published_at.desc())
    
    @staticmethod
    def get_by_category(category):
        """Возвращает статьи по категории."""
        return BlogPost.query.filter_by(is_published=True, category=category)\
            .order_by(BlogPost.published_at.desc())


class ContentPlan(db.Model):
    """Контент-план для автоматических публикаций."""
    
    __tablename__ = 'content_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Тема статьи
    description = db.Column(db.Text)  # Краткое описание/заметки
    
    # Планирование
    category = db.Column(db.String(100), default='Trends')
    keywords = db.Column(db.JSON)  # ["ключевые", "слова"]
    scheduled_date = db.Column(db.Date)  # Когда опубликовать
    
    # Статус
    STATUS_PLANNED = 'planned'
    STATUS_GENERATING = 'generating'
    STATUS_REVIEW = 'review'
    STATUS_PUBLISHED = 'published'
    STATUS_CANCELLED = 'cancelled'
    
    status = db.Column(db.String(50), default=STATUS_PLANNED)
    
    # Связь с созданной статьёй
    blog_post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    blog_post = db.relationship('BlogPost', backref='content_plan')
    
    # Мета
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContentPlan {self.title}>'
    
    @staticmethod
    def get_pending():
        """Возвращает запланированные темы для генерации."""
        from datetime import date
        return ContentPlan.query.filter(
            ContentPlan.status == ContentPlan.STATUS_PLANNED,
            ContentPlan.scheduled_date <= date.today()
        ).all()
