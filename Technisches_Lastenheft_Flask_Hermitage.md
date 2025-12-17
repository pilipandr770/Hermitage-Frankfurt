# Technisches Lastenheft
## Neuentwicklung der Website: hermitage-frankfurt.de
## Python Flask Web Application

**Auftraggeber:** Hermitage Home & Design GmbH & Co KG  
**Standort:** Hanauer Landstraße 421, 60314 Frankfurt am Main  
**Datum:** 17. Dezember 2025  
**Version:** 2.0  
**Technologie:** Python Flask, HTML5, CSS3, JavaScript

---

## 1. Projektübersicht

### 1.1 Ausgangssituation
Die bestehende WordPress-Website hermitage-frankfurt.de ist technisch veraltet (letzte Aktualisierung 2020) und erfordert umfangreiche Modernisierung. Statt einer WordPress-Optimierung wird eine komplette Neuentwicklung mit Python Flask durchgeführt.

### 1.2 Projektziel
Entwicklung einer modernen, performanten und wartungsfreundlichen Website als Python Flask-Anwendung mit:
- Identischer visueller Gestaltung wie die bestehende Website
- Automatisch befülltem Blog-System
- KI-gestütztem Chatbot-Assistenten für Kundenberatung
- Produktkatalog mit intelligenter Suche

### 1.3 Vorteile der Flask-Lösung

| Aspekt | WordPress (alt) | Flask (neu) |
|--------|-----------------|-------------|
| Performance | Langsam (viele Plugins) | Schnell (leichtgewichtig) |
| Sicherheit | Plugin-Abhängigkeit | Volle Kontrolle |
| Updates | Ständige Wartung nötig | Stabil, weniger Updates |
| Anpassbarkeit | Begrenzt durch Themes | 100% flexibel |
| KI-Integration | Schwierig | Native Python-Unterstützung |
| Hosting-Kosten | Höher (PHP, MySQL) | Günstiger (Python, SQLite/PostgreSQL) |

---

## 2. Funktionale Anforderungen

### 2.1 Seitenstruktur (identisch zum Original)

```
hermitage-frankfurt.de/
│
├── / (Startseite)
│   ├── Hero-Bereich mit Slider
│   ├── Willkommenstext
│   └── Kategorieübersicht (Fliesen, Innenausstattung)
│
├── /fliesen/
│   ├── Übersichtsseite Fliesen
│   ├── /fliesen/offenbach/
│   ├── /fliesen/hanau/
│   ├── /fliesen/maintal/
│   ├── /fliesen/darmstadt/
│   └── /fliesen/aschaffenburg/
│
├── /innenausstattung/
│   └── Interior Design Übersicht
│
├── /interior-design/
│   └── Detailseite Interior Design
│
├── /ueber-uns/ (About)
│   └── Firmengeschichte, Team
│
├── /service/
│   └── Dienstleistungen
│
├── /trends/
│   └── Aktuelle Trends
│
├── /magazine/
│   └── Inspirationen & Artikel
│
├── /blog/ [NEU - Automatisch befüllt]
│   ├── /blog/<slug>/
│   └── Kategorien, Tags, Suche
│
├── /kontakt/
│   └── Kontaktformular, Karte, Öffnungszeiten
│
├── /impressum/
├── /datenschutz/
└── /cookie-richtlinie/
```

### 2.2 Hauptfunktionen

#### 2.2.1 Produktkatalog (Fliesen & Innenausstattung)
| Funktion | Beschreibung |
|----------|--------------|
| Produktliste | Übersicht aller Produkte mit Bildern |
| Produktdetails | Einzelansicht mit Beschreibung, Galerie |
| Kategorien | Filterung nach Typ, Stil, Einsatzbereich |
| Suche | Volltextsuche über Produkte |
| Favoriten | Merkliste für Kunden (Session-basiert) |

#### 2.2.2 Blog-System (NEU - Automatisch befüllt)
| Funktion | Beschreibung |
|----------|--------------|
| Auto-Content | KI-generierte Artikel zu Fliesen-Trends |
| RSS-Feed | Automatischer Import von Branchennews |
| Kategorien | Trends, Tipps, Projekte, News |
| SEO | Automatische Meta-Tags und Sitemap |
| Zeitplanung | Automatische Veröffentlichung |

#### 2.2.3 KI-Chatbot-Assistent (NEU)
| Funktion | Beschreibung |
|----------|--------------|
| Produktberatung | Beantwortet Fragen zu Fliesen und Produkten |
| Wissensbasis | Kennt alle Produkte, Preise, Eigenschaften |
| Mehrsprachig | Deutsch und Englisch |
| 24/7 Verfügbar | Automatische Kundenberatung |
| Lead-Generierung | Sammelt Kontaktdaten bei Interesse |
| Handover | Weiterleitung an echten Mitarbeiter |

### 2.3 Administrative Funktionen

| Funktion | Beschreibung |
|----------|--------------|
| Admin-Dashboard | Geschützter Bereich für Inhaltspflege |
| Produktverwaltung | CRUD für Produkte |
| Blog-Verwaltung | Artikel erstellen/bearbeiten |
| Medienverwaltung | Bilder hochladen und verwalten |
| Chatbot-Training | Wissensbasis aktualisieren |
| Analytics | Besucherstatistiken |

---

## 3. Technische Architektur

### 3.1 Technologie-Stack

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
├─────────────────────────────────────────────────────────┤
│  HTML5 │ CSS3 (Bootstrap 5) │ JavaScript │ HTMX        │
│  Jinja2 Templates │ Alpine.js (optional)               │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                      BACKEND                            │
├─────────────────────────────────────────────────────────┤
│  Python 3.11+ │ Flask 3.x │ SQLAlchemy │ Flask-Login   │
│  Flask-WTF │ Flask-Mail │ Flask-Caching                │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    KI-KOMPONENTEN                       │
├─────────────────────────────────────────────────────────┤
│  OpenAI API (GPT-4) │ LangChain │ Vector DB (ChromaDB) │
│  Whisper (optional für Voice) │ RAG für Produktdaten   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                     DATENBANK                           │
├─────────────────────────────────────────────────────────┤
│  PostgreSQL (Produktion) │ SQLite (Entwicklung)        │
│  Redis (Caching, Sessions)                              │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                      HOSTING                            │
├─────────────────────────────────────────────────────────┤
│  Option A: VPS (Hetzner, DigitalOcean)                 │
│  Option B: PaaS (Railway, Render, Fly.io)              │
│  Option C: Docker + STRATO VPS                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Projektstruktur

```
hermitage-frankfurt/
│
├── app/
│   ├── __init__.py              # Flask App Factory
│   ├── config.py                # Konfiguration
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py           # Produkt-Model
│   │   ├── category.py          # Kategorie-Model
│   │   ├── blog.py              # Blog-Artikel-Model
│   │   ├── page.py              # Statische Seiten
│   │   └── user.py              # Admin-Benutzer
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Hauptseiten
│   │   ├── products.py          # Produkt-Routen
│   │   ├── blog.py              # Blog-Routen
│   │   ├── contact.py           # Kontakt-Routen
│   │   ├── api.py               # API-Endpunkte
│   │   └── admin.py             # Admin-Bereich
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chatbot.py           # KI-Chatbot-Logik
│   │   ├── blog_generator.py    # Auto-Blog-Generator
│   │   ├── email.py             # E-Mail-Service
│   │   └── scraper.py           # Content-Migration
│   │
│   ├── templates/
│   │   ├── base.html            # Basis-Template
│   │   ├── components/
│   │   │   ├── navbar.html
│   │   │   ├── footer.html
│   │   │   ├── chatbot.html
│   │   │   └── product_card.html
│   │   ├── pages/
│   │   │   ├── home.html
│   │   │   ├── fliesen.html
│   │   │   ├── innenausstattung.html
│   │   │   ├── about.html
│   │   │   ├── contact.html
│   │   │   └── ...
│   │   ├── blog/
│   │   │   ├── index.html
│   │   │   └── post.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       └── ...
│   │
│   └── static/
│       ├── css/
│       │   ├── style.css        # Hauptstyles
│       │   └── components.css
│       ├── js/
│       │   ├── main.js
│       │   └── chatbot.js
│       └── images/
│           └── ... (migrierte Bilder)
│
├── migrations/                   # Datenbank-Migrationen
├── tests/                        # Unit & Integration Tests
├── scripts/
│   ├── migrate_content.py       # WordPress-Migration
│   └── seed_data.py             # Testdaten
│
├── .env                          # Umgebungsvariablen
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 3.3 Datenbank-Schema

```sql
-- Produkte (Fliesen, Innenausstattung)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    short_description VARCHAR(500),
    category_id INTEGER REFERENCES categories(id),
    price_range VARCHAR(100),
    images JSONB,
    specifications JSONB,
    seo_title VARCHAR(255),
    seo_description VARCHAR(500),
    is_featured BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Kategorien
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id),
    image VARCHAR(500),
    sort_order INTEGER DEFAULT 0
);

-- Blog-Artikel
CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT,
    excerpt VARCHAR(500),
    featured_image VARCHAR(500),
    author_id INTEGER REFERENCES users(id),
    category VARCHAR(100),
    tags JSONB,
    is_auto_generated BOOLEAN DEFAULT FALSE,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Statische Seiten
CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT,
    template VARCHAR(100) DEFAULT 'default',
    seo_title VARCHAR(255),
    seo_description VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE
);

-- Chatbot-Konversationen
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    messages JSONB,
    user_email VARCHAR(255),
    user_phone VARCHAR(50),
    is_converted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Admin-Benutzer
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'editor',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 4. KI-Chatbot-Spezifikation

### 4.1 Architektur

```
┌─────────────────────────────────────────────────────────┐
│                   BENUTZER-INTERFACE                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  💬 Chat-Widget (rechts unten auf jeder Seite)  │   │
│  │  - Minimierbar                                   │   │
│  │  - Nachrichtenverlauf                           │   │
│  │  - Schnellantworten                             │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   CHATBOT-BACKEND                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Nachricht empfangen                                │
│  2. Intent erkennen (Produktfrage, Kontakt, etc.)      │
│  3. Relevante Produkte aus Vektor-DB suchen (RAG)      │
│  4. Prompt mit Kontext an GPT-4 senden                 │
│  5. Antwort generieren und zurücksenden                │
│                                                         │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    WISSENSBASIS                         │
├─────────────────────────────────────────────────────────┤
│  ChromaDB / Pinecone (Vektor-Datenbank)                │
│  ├── Alle Produktbeschreibungen (embeddings)           │
│  ├── FAQ-Antworten                                     │
│  ├── Firmeninformationen                               │
│  └── Preisrichtlinien                                  │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Beispiel-Dialoge

```
Kunde: "Welche Fliesen eignen sich für ein kleines Badezimmer?"

Bot: "Für kleine Badezimmer empfehle ich helle, großformatige Fliesen 
     (60x60 cm oder größer) – sie lassen den Raum optisch größer wirken. 
     
     Besonders beliebt sind:
     • Marmor-Optik Fliesen (elegant, zeitlos)
     • Metro-Fliesen (klassisch, vielseitig)
     • Holzoptik-Fliesen (warm, gemütlich)
     
     Möchten Sie unseren Showroom in der Hanauer Landstraße besuchen? 
     Ich kann gerne einen Beratungstermin für Sie vereinbaren! 📅"

---

Kunde: "Was kostet die Verlegung?"

Bot: "Die Verlegungskosten hängen von verschiedenen Faktoren ab:
     
     • Fliesengröße und -format
     • Untergrund und Vorbereitung
     • Verlegemuster (diagonal ist aufwändiger)
     
     Bei Hermitage bieten wir Komplettlösungen aus einer Hand – 
     von der Beratung bis zur fertigen Verlegung.
     
     Für ein individuelles Angebot können Sie uns erreichen:
     📞 069 90475570
     📧 info@hermitage-frankfurt.de
     
     Soll ich Ihre Kontaktdaten aufnehmen für einen Rückruf?"
```

### 4.3 System-Prompt

```python
SYSTEM_PROMPT = """
Du bist der virtuelle Assistent von Hermitage Frankfurt, einem exklusiven 
Fliesen- und Innenausstattungsfachgeschäft in Frankfurt am Main.

DEINE ROLLE:
- Freundliche, kompetente Beratung zu Fliesen und Innenausstattung
- Beantwortung von Fragen zu Produkten, Trends und Verlegung
- Terminvereinbarung für Showroom-Besuche
- Lead-Generierung durch Sammeln von Kontaktdaten

FIRMENDATEN:
- Name: Hermitage Home & Design GmbH & Co KG
- Adresse: Hanauer Landstraße 421, 60314 Frankfurt am Main
- Telefon: 069 90475570
- E-Mail: info@hermitage-frankfurt.de
- Gegründet: 1998 von Leonid Parhomowski

WICHTIGE REGELN:
1. Antworte immer auf Deutsch (außer der Kunde schreibt auf Englisch)
2. Sei freundlich und professionell
3. Empfehle bei konkreten Kaufinteressen einen Showroom-Besuch
4. Nenne nie konkrete Preise – verweise auf individuelle Beratung
5. Bei technischen Fragen außerhalb deines Wissens: Rückruf anbieten

PRODUKT-KONTEXT:
{product_context}
"""
```

---

## 5. Auto-Blog-System

### 5.1 Funktionsweise

```python
# Automatische Blog-Generierung (wöchentlich)
BLOG_TOPICS = [
    "Fliesentrends {year}",
    "Tipps für Badezimmergestaltung",
    "Naturstein vs. Keramikfliesen",
    "Pflege und Reinigung von Fliesen",
    "Farbtrends in der Innenausstattung",
    "Großformatige Fliesen: Vorteile",
    "Vintage-Fliesen: Comeback des Retro-Stils",
    "Nachhaltige Materialien im Interior Design",
]

# Ablauf:
# 1. Cron-Job läuft jeden Montag um 9:00 Uhr
# 2. Wählt zufälliges Thema aus der Liste
# 3. Generiert 800-1200 Wörter mit GPT-4
# 4. Erstellt SEO-optimierten Titel und Meta-Description
# 5. Sucht passendes Stockfoto (Unsplash API)
# 6. Speichert als Entwurf zur Überprüfung
# 7. Sendet E-Mail-Benachrichtigung an Admin
```

### 5.2 RSS-Feed-Integration

```python
RSS_FEEDS = [
    "https://www.baulinks.de/rss/fliesen.xml",
    "https://www.schoener-wohnen.de/rss",
    # Weitere relevante Feeds
]

# Automatischer Import:
# - Täglich prüfen auf neue Artikel
# - Relevante Artikel zusammenfassen
# - Als Inspiration für eigene Artikel nutzen
```

---

## 6. Content-Migration

### 6.1 Zu migrierende Inhalte von WordPress

| Inhalt | Quelle | Ziel |
|--------|--------|------|
| Seitentexte | 47 WordPress-Seiten | Flask Pages |
| Produktbilder | wp-content/uploads | static/images |
| Produktbeschreibungen | Seiteninhalte | Datenbank |
| FAQ-Inhalte | Accordion-Elemente | FAQ-Tabelle |
| Kontaktdaten | Impressum | Config/Templates |
| SEO-Texte | Yoast Meta | Datenbank |

### 6.2 Migrations-Script

```python
# scripts/migrate_content.py
import requests
from bs4 import BeautifulSoup
from app.models import Page, Product

PAGES_TO_MIGRATE = [
    ("https://hermitage-frankfurt.de/", "home"),
    ("https://hermitage-frankfurt.de/fliesen/", "fliesen"),
    ("https://hermitage-frankfurt.de/innenausstattung/", "innenausstattung"),
    ("https://hermitage-frankfurt.de/about/", "about"),
    ("https://hermitage-frankfurt.de/kontakt/", "contact"),
    ("https://hermitage-frankfurt.de/impressum/", "impressum"),
    ("https://hermitage-frankfurt.de/datenschutzerklaerung/", "datenschutz"),
    # ... weitere Seiten
]

def migrate_page(url, slug):
    """Migriert eine einzelne Seite."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extrahiere Inhalte
    title = soup.find('h1').text
    content = soup.find('main').get_text()
    images = [img['src'] for img in soup.find_all('img')]
    
    # Speichere in Datenbank
    page = Page(title=title, slug=slug, content=content)
    db.session.add(page)
    
    # Lade Bilder herunter
    for img_url in images:
        download_image(img_url, f"static/images/{slug}/")
```

---

## 7. Entwicklungsplan

### Phase 1: Setup & Grundstruktur (Woche 1)
| Tag | Aufgabe | Stunden |
|-----|---------|---------|
| 1 | Projekt-Setup, Git, virtuelle Umgebung | 2 |
| 1 | Flask-App-Struktur anlegen | 3 |
| 2 | Datenbank-Modelle erstellen | 4 |
| 2 | Basis-Templates (base.html, navbar, footer) | 4 |
| 3 | Statische Seiten-Routen | 3 |
| 3 | CSS-Framework einrichten (Bootstrap) | 3 |
| 4 | Content-Migration-Script | 4 |
| 4 | Bilder migrieren | 2 |
| 5 | Startseite fertigstellen | 4 |
| **Gesamt** | | **29 Std.** |

### Phase 2: Kernseiten (Woche 2)
| Tag | Aufgabe | Stunden |
|-----|---------|---------|
| 1 | Fliesen-Übersichtsseite | 4 |
| 1 | Fliesen-Unterseiten (Städte) | 4 |
| 2 | Innenausstattung-Seiten | 4 |
| 2 | Interior Design Seite | 3 |
| 3 | Über Uns Seite | 3 |
| 3 | Service-Seite | 3 |
| 4 | Kontaktseite + Formular | 4 |
| 4 | E-Mail-Versand einrichten | 2 |
| 5 | Impressum, Datenschutz | 2 |
| 5 | Cookie-Banner (DSGVO) | 2 |
| **Gesamt** | | **31 Std.** |

### Phase 3: Produktkatalog (Woche 3)
| Tag | Aufgabe | Stunden |
|-----|---------|---------|
| 1 | Produkt-Model erweitern | 3 |
| 1 | Produkt-Admin-CRUD | 5 |
| 2 | Produktliste mit Filtern | 5 |
| 2 | Produktdetailseite | 3 |
| 3 | Bildergalerie-Komponente | 4 |
| 3 | Suche implementieren | 3 |
| 4 | Favoriten/Merkliste | 4 |
| 5 | Responsive Optimierung | 4 |
| **Gesamt** | | **31 Std.** |

### Phase 4: KI-Chatbot (Woche 4)
| Tag | Aufgabe | Stunden |
|-----|---------|---------|
| 1 | OpenAI API Integration | 3 |
| 1 | LangChain Setup | 3 |
| 2 | Vektor-Datenbank (ChromaDB) | 4 |
| 2 | Produkte embedden | 3 |
| 3 | Chat-Backend-Logik | 5 |
| 3 | RAG-Pipeline | 3 |
| 4 | Chat-Widget Frontend | 5 |
| 5 | WebSocket-Integration | 4 |
| 5 | Testing & Feintuning | 2 |
| **Gesamt** | | **32 Std.** |

### Phase 5: Auto-Blog (Woche 5)
| Tag | Aufgabe | Stunden |
|-----|---------|---------|
| 1 | Blog-Model & Routen | 4 |
| 1 | Blog-Übersicht & Detailseite | 4 |
| 2 | Auto-Generation-Service | 5 |
| 2 | RSS-Feed-Parser | 3 |
| 3 | Scheduling (APScheduler) | 3 |
| 3 | Admin-Blog-Verwaltung | 4 |
| 4 | SEO-Optimierung | 3 |
| 4 | Sitemap-Generator | 2 |
| 5 | Testing & Bugfixes | 4 |
| **Gesamt** | | **32 Std.** |

### Phase 6: Admin & Deployment (Woche 6)
| Tag | Aufgabe | Stunden |
|-----|---------|---------|
| 1 | Admin-Dashboard | 4 |
| 1 | Benutzer-Authentifizierung | 3 |
| 2 | Analytics-Integration | 3 |
| 2 | Performance-Optimierung | 4 |
| 3 | Docker-Setup | 3 |
| 3 | CI/CD Pipeline | 3 |
| 4 | Server-Deployment | 4 |
| 4 | SSL/HTTPS einrichten | 2 |
| 5 | DNS-Umstellung | 1 |
| 5 | Finales Testing | 4 |
| 5 | Dokumentation | 3 |
| **Gesamt** | | **34 Std.** |

---

## 8. Kostenvoranschlag

### 8.1 Entwicklungskosten

| Phase | Stunden | Kosten (85€/Std.) |
|-------|---------|-------------------|
| Setup & Grundstruktur | 29 | 2.465 € |
| Kernseiten | 31 | 2.635 € |
| Produktkatalog | 31 | 2.635 € |
| KI-Chatbot | 32 | 2.720 € |
| Auto-Blog | 32 | 2.720 € |
| Admin & Deployment | 34 | 2.890 € |
| **Gesamt Entwicklung** | **189 Std.** | **16.065 €** |

### 8.2 Zusätzliche Kosten

| Posten | Kosten | Zeitraum |
|--------|--------|----------|
| OpenAI API (GPT-4) | ~50-100 € | monatlich |
| Hosting (VPS) | 20-50 € | monatlich |
| Domain (falls neu) | 15 € | jährlich |
| SSL-Zertifikat | 0 € (Let's Encrypt) | - |
| Stockfotos (optional) | 0-100 € | einmalig |

### 8.3 Gesamtkosten

| Variante | Einmalig | Monatlich |
|----------|----------|-----------|
| **Entwicklung komplett** | **16.000-18.000 €** | - |
| **Hosting & KI** | - | **70-150 €** |
| **Wartung (optional)** | - | **200-400 €** |

### 8.4 Vergleich mit WordPress-Optimierung

| Aspekt | WordPress-Optimierung | Flask-Neuentwicklung |
|--------|----------------------|---------------------|
| Einmalkosten | 4.000-6.000 € | 16.000-18.000 € |
| Monatliche Kosten | 50-100 € | 70-150 € |
| KI-Chatbot | Schwer integrierbar | ✅ Native |
| Auto-Blog | Plugin nötig | ✅ Native |
| Zukunftssicherheit | Mittel | Hoch |
| Performance | Mittel | Hoch |
| Wartungsaufwand | Hoch | Niedrig |

---

## 9. Hosting-Empfehlung

### Option A: Hetzner Cloud (Empfohlen für Deutschland)
```
Server: CX21 (2 vCPU, 4 GB RAM)
Kosten: ~8 €/Monat
+ Volume: 20 GB (~2 €/Monat)
+ Backups: ~2 €/Monat
= Gesamt: ~12 €/Monat
```

### Option B: Railway (Einfachstes Setup)
```
Starter Plan: 5 $/Monat Basis
+ Usage: ~10-20 $/Monat
= Gesamt: ~15-25 $/Monat
```

### Option C: Docker auf bestehendem STRATO
```
Falls STRATO VPS vorhanden:
- Docker installieren
- Anwendung deployen
- Keine zusätzlichen Kosten
```

---

## 10. Nächste Schritte

### Sofort zu erledigen:
- [ ] Projektordner erstellen
- [ ] Git-Repository initialisieren
- [ ] Virtuelle Umgebung einrichten
- [ ] Flask-Grundgerüst aufsetzen
- [ ] Content-Migration starten

### Diese Woche:
- [ ] Alle Bilder von WordPress herunterladen
- [ ] Texte aller Seiten exportieren
- [ ] Basis-Templates erstellen
- [ ] Erste Seiten implementieren

### Zu klären mit Auftraggeber:
- [ ] OpenAI API Budget genehmigen
- [ ] Hosting-Entscheidung treffen
- [ ] Design-Anpassungen besprechen
- [ ] Prioritäten für Features festlegen

---

## 11. Anhang: Schnellstart-Befehle

```bash
# Projekt erstellen
mkdir hermitage-frankfurt
cd hermitage-frankfurt
python -m venv venv
venv\Scripts\activate  # Windows
pip install flask flask-sqlalchemy python-dotenv

# Grundstruktur
mkdir -p app/{models,routes,services,templates,static}
touch app/__init__.py app/config.py

# Git initialisieren
git init
echo "venv/\n.env\n__pycache__/" > .gitignore

# Entwicklungsserver starten
flask run --debug
```

---

*Dieses Lastenheft dient als Grundlage für die Entwicklung der neuen Flask-basierten Website für Hermitage Frankfurt.*

**Erstellt am:** 17. Dezember 2025  
**Version:** 2.0 – Flask-Neuentwicklung
