# Hermitage Frankfurt - Website

Витринный сайт для Hermitage Home & Design GmbH & Co KG - премиум поставщика плитки, натурального камня и интерьерных решений во Франкфурте.

## 🌟 Возможности

- **Витринный сайт** - представление продукции и услуг компании
- **AI Чатбот** - консультант на базе GPT-4 для помощи посетителям
- **Авто-блог** - автоматическая генерация SEO-контента
- **Админ-панель** - управление чатботом и контент-планом

## 🛠 Технологии

- **Backend**: Python 3.11+, Flask 3.x
- **Database**: SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Bootstrap 5, Jinja2
- **AI**: OpenAI GPT-4

## 📦 Установка

### 1. Клонирование и виртуальное окружение

```bash
cd hermitage-frankfurt.de
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка окружения

```bash
copy .env.example .env
# Отредактируйте .env и добавьте:
# - SECRET_KEY
# - OPENAI_API_KEY
# - Настройки почты
```

### 4. Инициализация базы данных

```bash
flask init-db
flask create-admin
flask seed-data
```

### 5. Запуск

```bash
# Разработка
python run.py

# Или
flask run --debug
```

Сайт будет доступен по адресу: http://localhost:5000

## 📁 Структура проекта

```
hermitage-frankfurt.de/
├── app/
│   ├── __init__.py         # Application factory
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # Flask blueprints
│   ├── services/           # Business logic (chatbot, blog generator)
│   ├── templates/          # Jinja2 templates
│   └── static/             # CSS, JS, images
├── config.py               # Configuration
├── run.py                  # Entry point
├── requirements.txt
└── .env.example
```

## 🔧 Команды CLI

```bash
flask init-db       # Создать таблицы БД
flask create-admin  # Создать администратора
flask seed-data     # Заполнить начальными данными
```

## 🚀 Деплой (Production)

### STRATO или Hetzner VPS

1. Установите Python 3.11+
2. Настройте PostgreSQL
3. Используйте Gunicorn + Nginx

```bash
# Gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 run:app
```

### Nginx конфигурация

```nginx
server {
    listen 80;
    server_name hermitage-frankfurt.de;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/app/static;
        expires 30d;
    }
}
```

## 📧 Контакты

**Hermitage Home & Design GmbH & Co KG**  
Hanauer Landstraße 421  
60314 Frankfurt am Main  
Tel: 069 90475570

---

© 2025 Hermitage Frankfurt. All rights reserved.
