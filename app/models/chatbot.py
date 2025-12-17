"""
Модели для чатбота
"""

from datetime import datetime
from app import db


class ChatbotInstruction(db.Model):
    """Инструкции и знания для чатбота."""
    
    __tablename__ = 'chatbot_instructions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    
    # Тип инструкции
    TYPE_PRODUCT = 'product'        # Информация о товаре
    TYPE_FAQ = 'faq'                # Частые вопросы
    TYPE_POLICY = 'policy'          # Политики (доставка, возврат)
    TYPE_COMPANY = 'company'        # Информация о компании
    TYPE_INSTRUCTION = 'instruction' # Поведенческие инструкции
    
    instruction_type = db.Column(db.String(50), default=TYPE_FAQ)
    
    # Содержимое
    content = db.Column(db.Text, nullable=False)
    
    # Для поиска
    keywords = db.Column(db.JSON)  # Ключевые слова для RAG
    
    # Мета
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=0)  # Высший приоритет = важнее
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatbotInstruction {self.title}>'
    
    @staticmethod
    def get_all_active():
        """Возвращает все активные инструкции."""
        return ChatbotInstruction.query.filter_by(is_active=True)\
            .order_by(ChatbotInstruction.priority.desc()).all()
    
    @staticmethod
    def get_by_type(instruction_type):
        """Возвращает инструкции по типу."""
        return ChatbotInstruction.query.filter_by(
            is_active=True, 
            instruction_type=instruction_type
        ).order_by(ChatbotInstruction.priority.desc()).all()
    
    def to_context(self):
        """Конвертирует в строку для контекста чатбота."""
        return f"[{self.instruction_type.upper()}] {self.title}:\n{self.content}"


class ChatSession(db.Model):
    """Сессии чата с посетителями."""
    
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    
    # История сообщений
    messages = db.Column(db.JSON)  # [{"role": "user/assistant", "content": "..."}]
    
    # Контактные данные (если пользователь оставил)
    user_name = db.Column(db.String(255))
    user_email = db.Column(db.String(255))
    user_phone = db.Column(db.String(50))
    
    # Аналитика
    page_url = db.Column(db.String(500))  # На какой странице начат чат
    is_lead = db.Column(db.Boolean, default=False)  # Оставил контакты?
    
    # Мета
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatSession {self.session_id}>'
    
    def add_message(self, role, content):
        """Добавляет сообщение в историю."""
        if self.messages is None:
            self.messages = []
        
        # Создаём новый список чтобы SQLAlchemy увидел изменение
        new_messages = list(self.messages)
        new_messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow().isoformat()
        })
        self.messages = new_messages
    
    def get_messages_for_api(self):
        """Форматирует сообщения для OpenAI API."""
        if not self.messages:
            return []
        return [{'role': m['role'], 'content': m['content']} for m in self.messages]
    
    def mark_as_lead(self, name=None, email=None, phone=None):
        """Отмечает сессию как лид."""
        self.is_lead = True
        if name:
            self.user_name = name
        if email:
            self.user_email = email
        if phone:
            self.user_phone = phone
