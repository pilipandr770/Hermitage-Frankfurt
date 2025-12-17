"""
Скрипт для инициализации схемы PostgreSQL на Render.com

Запуск:
    python scripts/init_postgres_schema.py

Этот скрипт создаёт отдельную схему 'hermitage' в базе данных,
чтобы изолировать таблицы от других проектов.
"""

import os
import sys
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Получаем URL базы данных
DATABASE_URL = os.environ.get('DATABASE_URL')
SCHEMA_NAME = os.environ.get('DATABASE_SCHEMA', 'hermitage')

if not DATABASE_URL or 'postgresql' not in DATABASE_URL:
    print("ERROR: DATABASE_URL не настроен или не является PostgreSQL")
    print("Убедитесь что в .env указан PostgreSQL URL")
    sys.exit(1)

print(f"Подключение к: {DATABASE_URL[:50]}...")
print(f"Схема: {SCHEMA_NAME}")

try:
    import psycopg2
    from psycopg2 import sql
    
    # Подключаемся к базе
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Создаём схему если её нет
    print(f"\n1. Создание схемы '{SCHEMA_NAME}'...")
    cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
        sql.Identifier(SCHEMA_NAME)
    ))
    print(f"   ✓ Схема '{SCHEMA_NAME}' готова")
    
    # Проверяем существующие таблицы в схеме
    print(f"\n2. Проверка таблиц в схеме '{SCHEMA_NAME}'...")
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = %s
        ORDER BY table_name
    """, (SCHEMA_NAME,))
    
    tables = cur.fetchall()
    if tables:
        print(f"   Найдено таблиц: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("   Таблиц пока нет (будут созданы при первом запуске)")
    
    # Закрываем соединение
    cur.close()
    conn.close()
    
    print("\n" + "="*50)
    print("✓ Схема PostgreSQL успешно инициализирована!")
    print("="*50)
    print(f"\nТеперь можно деплоить на Render.com")
    print(f"В Environment Variables на Render добавьте:")
    print(f"  DATABASE_URL = {DATABASE_URL}")
    print(f"  DATABASE_SCHEMA = {SCHEMA_NAME}")
    
except ImportError:
    print("ERROR: psycopg2 не установлен")
    print("Установите: pip install psycopg2-binary")
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
