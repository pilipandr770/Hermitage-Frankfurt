"""
Модель администратора для админки
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


class Admin(UserMixin, db.Model):
    """Администратор сайта."""
    
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    
    # Мета
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Admin {self.username}>'
    
    def set_password(self, password):
        """Устанавливает хэш пароля."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверяет пароль."""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Обновляет время последнего входа."""
        self.last_login = datetime.utcnow()


@login_manager.user_loader
def load_user(user_id):
    """Загрузчик пользователя для Flask-Login с обработкой ошибок БД."""
    from app import db
    try:
        return db.session.get(Admin, int(user_id))
    except Exception:
        # При ошибке соединения откатываем транзакцию
        db.session.rollback()
        try:
            return db.session.get(Admin, int(user_id))
        except Exception:
            return None
