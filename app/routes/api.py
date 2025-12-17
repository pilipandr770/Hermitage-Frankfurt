"""
API маршруты для чатбота
"""

from flask import Blueprint, request, jsonify, session
import uuid
from app import db
from app.models import ChatSession
from app.services.chatbot import ChatbotService

api_bp = Blueprint('api', __name__)


@api_bp.route('/chat', methods=['POST'])
def chat():
    """Обработка сообщений чатбота."""
    # Отладка - что приходит
    print("=== CHAT REQUEST ===")
    print(f"Content-Type: {request.content_type}")
    print(f"Data: {request.data}")
    
    # Получаем JSON данные (force=True игнорирует Content-Type)
    data = request.get_json(force=True, silent=True)
    print(f"Parsed JSON: {data}")
    
    if not data:
        return jsonify({'error': 'Invalid JSON data', 'received': str(request.data)}), 400
    
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Message is required', 'data': data}), 400
    
    page_url = data.get('page_url', '')
    
    # Получаем или создаём сессию чата
    session_id = session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['chat_session_id'] = session_id
    
    try:
        # Находим или создаём запись в БД
        chat_session = ChatSession.query.filter_by(session_id=session_id).first()
        if not chat_session:
            chat_session = ChatSession(session_id=session_id, page_url=page_url)
            db.session.add(chat_session)
        
        # Добавляем сообщение пользователя
        chat_session.add_message('user', user_message)
        
        # Получаем ответ от AI
        chatbot = ChatbotService()
        assistant_response = chatbot.get_response(
            user_message=user_message,
            chat_history=chat_session.get_messages_for_api()
        )
        
        # Добавляем ответ ассистента
        chat_session.add_message('assistant', assistant_response)
        
        db.session.commit()
        
        return jsonify({
            'response': assistant_response,
            'session_id': session_id
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'response': 'Entschuldigung, es gab einen technischen Fehler. Bitte rufen Sie uns an: 069 90475570',
            'error': str(e)
        }), 200  # Возвращаем 200 чтобы пользователь увидел сообщение


@api_bp.route('/chat/lead', methods=['POST'])
def submit_lead():
    """Сохранение контактных данных из чата."""
    data = request.get_json()
    
    session_id = session.get('chat_session_id')
    if not session_id:
        return jsonify({'error': 'No active chat session'}), 400
    
    chat_session = ChatSession.query.filter_by(session_id=session_id).first()
    if not chat_session:
        return jsonify({'error': 'Chat session not found'}), 404
    
    # Сохраняем данные
    chat_session.mark_as_lead(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone')
    )
    db.session.commit()
    
    # TODO: Отправить уведомление администратору
    
    return jsonify({'success': True, 'message': 'Vielen Dank! Wir melden uns bei Ihnen.'})


@api_bp.route('/chat/reset', methods=['POST'])
def reset_chat():
    """Сброс сессии чата."""
    session.pop('chat_session_id', None)
    return jsonify({'success': True})
