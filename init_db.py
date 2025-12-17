"""
Скрипт инициализации базы данных PostgreSQL
Создаёт схему 'hermitage' и все таблицы
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def init_database():
    """Инициализирует базу данных."""
    
    database_url = os.environ.get('DATABASE_URL')
    schema_name = os.environ.get('DATABASE_SCHEMA', 'hermitage')
    
    if not database_url:
        print("ERROR: DATABASE_URL not set in .env")
        sys.exit(1)
    
    print(f"Database URL: {database_url[:50]}...")
    print(f"Schema: {schema_name}")
    
    # Для PostgreSQL создаём схему
    if database_url.startswith('postgresql'):
        print("\n1. Creating schema if not exists...")
        
        import psycopg2
        from psycopg2 import sql
        
        # Подключаемся напрямую для создания схемы
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        try:
            # Создаём схему
            cursor.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                    sql.Identifier(schema_name)
                )
            )
            print(f"   ✅ Schema '{schema_name}' created/exists")
            
        except Exception as e:
            print(f"   ❌ Error creating schema: {e}")
        finally:
            cursor.close()
            conn.close()
    
    # Создаём таблицы через SQLAlchemy
    print("\n2. Creating tables...")
    
    from app import create_app, db
    
    app = create_app('production')
    
    with app.app_context():
        # Создаём все таблицы
        db.create_all()
        print("   ✅ All tables created")
        
        # Показываем созданные таблицы
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        if database_url.startswith('postgresql'):
            tables = inspector.get_table_names(schema=schema_name)
        else:
            tables = inspector.get_table_names()
        
        print(f"\n3. Tables in schema '{schema_name}':")
        for table in tables:
            print(f"   - {table}")
    
    print("\n✅ Database initialization complete!")


def create_admin():
    """Создаёт администратора."""
    from app import create_app, db
    from app.models import Admin
    
    app = create_app('production')
    
    with app.app_context():
        # Проверяем есть ли уже админ
        existing = Admin.query.first()
        if existing:
            print(f"Admin already exists: {existing.username}")
            return
        
        # Создаём нового
        admin = Admin(
            username='admin',
            email='info@hermitage-frankfurt.de',
            is_active=True
        )
        admin.set_password('Hermitage2024!')  # Сменить после первого входа!
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin created:")
        print("   Username: admin")
        print("   Password: Hermitage2024!")
        print("   ⚠️  Change password after first login!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'admin':
        create_admin()
    else:
        init_database()
        print("\n" + "="*50)
        create_admin()
