#!/usr/bin/env python3
"""
Hermitage Frankfurt - Flask Application Entry Point
"""

import os
from app import create_app, db
from app.models import Admin, Page, BlogPost, ChatbotInstruction

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Create application
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Context for flask shell command."""
    return {
        'db': db,
        'Admin': Admin,
        'Page': Page,
        'BlogPost': BlogPost,
        'ChatbotInstruction': ChatbotInstruction
    }


@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


@app.cli.command('create-admin')
def create_admin():
    """Create admin user."""
    from getpass import getpass
    
    username = input('Username: ')
    email = input('Email: ')
    password = getpass('Password: ')
    name = input('Name (optional): ') or None
    
    admin = Admin(
        username=username,
        email=email,
        name=name
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print(f'Admin user "{username}" created!')


@app.cli.command('seed-data')
def seed_data():
    """Seed database with initial data."""
    
    # Default chatbot instructions
    instructions = [
        {
            'title': 'Unternehmensinfo',
            'instruction_type': 'company',
            'content': '''Hermitage Home & Design GmbH & Co KG ist ein Premium-Anbieter für Fliesen, 
            Naturstein und Innenausstattung in Frankfurt am Main. Gegründet 1998 von Leonid Parhomowski.
            
            Adresse: Hanauer Landstraße 421, 60314 Frankfurt am Main
            Telefon: 069 90475570
            
            Showroom mit über 1000m² Ausstellungsfläche.''',
            'priority': 100,
            'keywords': ['hermitage', 'firma', 'unternehmen', 'adresse', 'kontakt', 'öffnungszeiten']
        },
        {
            'title': 'Produktsortiment Fliesen',
            'instruction_type': 'product',
            'content': '''Wir bieten ein umfangreiches Sortiment an hochwertigen Fliesen:
            
            - Keramikfliesen für Boden und Wand
            - Naturstein (Marmor, Granit, Travertin)
            - Großformatige Fliesen
            - Mosaikfliesen
            - Fliesen in Holzoptik
            - Outdoor-Fliesen für Terrassen
            
            Alle Produkte von namhaften italienischen und spanischen Herstellern.''',
            'priority': 90,
            'keywords': ['fliesen', 'keramik', 'marmor', 'granit', 'naturstein', 'mosaik']
        },
        {
            'title': 'Beratung und Service',
            'instruction_type': 'faq',
            'content': '''Wir bieten kostenlose Beratung in unserem Showroom.
            
            - Persönliche Beratung durch Experten
            - 3D-Visualisierung Ihrer Projekte
            - Musterversand möglich
            - Lieferung deutschlandweit
            - Verlegung durch Partner-Handwerker
            
            Vereinbaren Sie einen Beratungstermin!''',
            'priority': 80,
            'keywords': ['beratung', 'termin', 'service', 'lieferung', 'verlegung']
        },
        {
            'title': 'Verhaltensanweisung',
            'instruction_type': 'instruction',
            'content': '''Du bist ein freundlicher und kompetenter Berater.
            
            Regeln:
            - Antworte immer auf Deutsch
            - Sei höflich und professionell
            - Bei komplexen Fragen: Empfehle Besuch im Showroom oder Telefonat
            - Sammle Kontaktdaten für Rückruf bei Interesse
            - Erwähne unsere kostenlose Beratung
            - Maximal 3-4 Sätze pro Antwort''',
            'priority': 100,
            'keywords': []
        }
    ]
    
    for instr_data in instructions:
        keywords = instr_data.pop('keywords')
        instruction = ChatbotInstruction(**instr_data)
        instruction.keywords = keywords
        db.session.add(instruction)
    
    # Default pages content
    pages = [
        {
            'slug': 'home',
            'title': 'Willkommen bei Hermitage',
            'meta_title': 'Hermitage Frankfurt - Premium Fliesen & Naturstein',
            'meta_description': 'Ihr Spezialist für hochwertige Fliesen, Naturstein und exklusive Innenausstattung in Frankfurt. Besuchen Sie unseren 1000m² Showroom.'
        },
        {
            'slug': 'fliesen',
            'title': 'Fliesen',
            'meta_title': 'Premium Fliesen Frankfurt | Hermitage Home & Design',
            'meta_description': 'Entdecken Sie unser exklusives Sortiment an Keramik- und Natursteinfliesen. Italienisches Design, höchste Qualität.'
        },
        {
            'slug': 'innenausstattung',
            'title': 'Innenausstattung',
            'meta_title': 'Exklusive Innenausstattung Frankfurt | Hermitage',
            'meta_description': 'Luxuriöse Innenausstattung für Ihr Zuhause. Möbel, Dekoration und Interior Design von Hermitage Frankfurt.'
        }
    ]
    
    for page_data in pages:
        page = Page(**page_data)
        db.session.add(page)
    
    db.session.commit()
    print('Database seeded with initial data!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
