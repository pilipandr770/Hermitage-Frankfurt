/* Hermitage Frankfurt - Chatbot Widget */

class HermitageChatbot {
    constructor() {
        this.isOpen = false;
        this.isLoading = false;
        this.init();
    }
    
    init() {
        // Элементы
        this.toggleBtn = document.getElementById('chatbot-toggle');
        this.window = document.getElementById('chatbot-window');
        this.minimizeBtn = document.getElementById('chatbot-minimize');
        this.messagesContainer = document.getElementById('chatbot-messages');
        this.form = document.getElementById('chatbot-form');
        this.inputField = document.getElementById('chatbot-input-field');
        this.iconOpen = document.getElementById('chat-icon-open');
        this.iconClose = document.getElementById('chat-icon-close');
        
        if (!this.toggleBtn) {
            console.error('Chatbot: Toggle button not found');
            return;
        }
        
        this.bindEvents();
        console.log('Chatbot initialized');
    }
    
    bindEvents() {
        // Открытие/закрытие чата
        this.toggleBtn.addEventListener('click', () => this.toggle());
        
        // Минимизация
        if (this.minimizeBtn) {
            this.minimizeBtn.addEventListener('click', () => this.close());
        }
        
        // Отправка сообщения
        if (this.form) {
            this.form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }
        
        // Quick replies
        document.querySelectorAll('.quick-reply').forEach(btn => {
            btn.addEventListener('click', () => {
                const message = btn.dataset.message;
                if (message) {
                    this.inputField.value = message;
                    this.sendMessage();
                }
            });
        });
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.isOpen = true;
        this.window.classList.remove('d-none');
        this.window.classList.add('active');
        this.iconOpen.classList.add('d-none');
        this.iconClose.classList.remove('d-none');
        this.inputField.focus();
        
        // Прокрутка вниз
        this.scrollToBottom();
    }
    
    close() {
        this.isOpen = false;
        this.window.classList.remove('active');
        this.window.classList.add('d-none');
        this.iconOpen.classList.remove('d-none');
        this.iconClose.classList.add('d-none');
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
    
    addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user' : 'assistant'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = this.formatMessage(content);
        
        messageDiv.appendChild(contentDiv);
        this.messagesContainer.appendChild(messageDiv);
        
        // Скрываем quick replies после первого сообщения пользователя
        if (isUser) {
            const quickReplies = document.querySelector('.quick-replies');
            if (quickReplies) {
                quickReplies.style.display = 'none';
            }
        }
        
        this.scrollToBottom();
    }
    
    formatMessage(text) {
        // Превращаем переносы строк в <br>
        let formatted = text.replace(/\n/g, '<br>');
        
        // Превращаем **text** в <strong>text</strong>
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Превращаем ссылки в кликабельные
        formatted = formatted.replace(
            /(https?:\/\/[^\s<]+)/g, 
            '<a href="$1" target="_blank" rel="noopener">$1</a>'
        );
        
        // Превращаем номера телефонов в кликабельные
        formatted = formatted.replace(
            /(\d{3,4}\s?\d{6,8})/g,
            '<a href="tel:$1">$1</a>'
        );
        
        return formatted;
    }
    
    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message assistant typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        `;
        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTyping() {
        const typing = document.getElementById('typing-indicator');
        if (typing) {
            typing.remove();
        }
    }
    
    async sendMessage() {
        const message = this.inputField.value.trim();
        if (!message || this.isLoading) return;
        
        // Добавляем сообщение пользователя
        this.addMessage(message, true);
        this.inputField.value = '';
        this.inputField.disabled = true;
        this.isLoading = true;
        
        // Показываем индикатор набора
        this.showTyping();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    page_url: window.location.pathname
                })
            });
            
            this.hideTyping();
            
            if (response.ok) {
                const data = await response.json();
                this.addMessage(data.response);
            } else {
                this.addMessage('Entschuldigung, es gab einen Fehler. Bitte versuchen Sie es später erneut oder rufen Sie uns an: 069 90475570');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTyping();
            this.addMessage('Die Verbindung wurde unterbrochen. Bitte versuchen Sie es erneut oder kontaktieren Sie uns telefonisch: 069 90475570');
        } finally {
            this.isLoading = false;
            this.inputField.disabled = false;
            this.inputField.focus();
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.hermitageChatbot = new HermitageChatbot();
});
