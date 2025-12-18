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
            'seo_title': 'Hermitage Frankfurt – Premium Fliesen & Interior Design',
            'seo_description': 'Premium Fliesen Showroom Frankfurt ✓ Naturstein ✓ Feinsteinzeug ✓ Mosaik ✓ Innenausstattung ✓ 27 Jahre Erfahrung ✓ Kostenlose Beratung ☎ 069-90475570'
        },
        {
            'slug': 'fliesen',
            'title': 'Fliesen',
            'seo_title': 'Fliesen Frankfurt – Premium Kollektion | Hermitage',
            'seo_description': 'Exklusive Fliesen Frankfurt ✓ Feinsteinzeug ✓ Naturstein ✓ Marmor ✓ Mosaik ✓ 500m² Showroom ✓ Persönliche Beratung ✓ Seit 1998 Ihr Fliesenexperte'
        },
        {
            'slug': 'innenausstattung',
            'title': 'Innenausstattung',
            'seo_title': 'Innenausstattung Frankfurt – Badmöbel & Interior Design',
            'seo_description': 'Komplette Innenausstattung Frankfurt ✓ Badmöbel ✓ Armaturen ✓ Beleuchtung ✓ Interior Design ✓ 500m² Showroom ✓ Individuelle Beratung seit 1998'
        },
        {
            'slug': 'contact',
            'title': 'Kontakt',
            'seo_title': 'Kontakt Hermitage Frankfurt – Showroom & Beratung',
            'seo_description': 'Kontaktieren Sie Hermitage Frankfurt ✓ Showroom Hanauer Landstraße 421 ✓ ☎ 069-90475570 ✓ Öffnungszeiten ✓ Anfahrt ✓ Kostenlose Beratung vereinbaren'
        },
        {
            'slug': 'about',
            'title': 'Über uns',
            'seo_title': 'Über Hermitage Frankfurt – 27 Jahre Fliesenexpertise',
            'seo_description': 'Hermitage Frankfurt seit 1998 ✓ Premium Fliesen & Innenausstattung ✓ 1000m² Showroom ✓ Gegründet von Leonid Parhomowski ✓ Ihr vertrauensvoller Partner'
        },
        {
            'slug': 'service',
            'title': 'Service',
            'seo_title': 'Service Hermitage Frankfurt – Beratung & Verlegung',
            'seo_description': 'Umfassender Service Hermitage Frankfurt ✓ Kostenlose Beratung ✓ 3D-Planung ✓ Professionelle Verlegung ✓ Musterservice ✓ Deutschlandweite Lieferung'
        },
        {
            'slug': 'badsanierung-leitfaden',
            'title': 'Badsanierung Leitfaden',
            'seo_title': 'Badsanierung Frankfurt – Kompletter Leitfaden 2025',
            'seo_description': 'Badsanierung Frankfurt 2025 ✓ Kompletter Leitfaden ✓ Kosten ✓ Planung ✓ Materialien ✓ Ablauf ✓ Experten-Tipps ✓ 27 Jahre Erfahrung ✓ Jetzt beraten lassen'
        },
        {
            'slug': 'fliesenarten-badezimmer',
            'title': 'Fliesenarten für Badezimmer',
            'seo_title': 'Fliesenarten für Badezimmer – Kompletter Ratgeber 2025',
            'seo_description': 'Fliesenarten für Badezimmer 2025 ✓ Keramik ✓ Porzellan ✓ Naturstein ✓ Mosaik ✓ Kosten ✓ Vor- & Nachteile ✓ Pflege ✓ Experten-Tipps ✓ Jetzt beraten lassen'
        }
    ]


    
    db.session.commit()
    print('Database seeded with initial data!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
