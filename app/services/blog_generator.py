"""
Сервис автоматической генерации блог-статей
"""

import os
import re
from datetime import datetime
from slugify import slugify
from openai import OpenAI
from app import db
from app.models import BlogPost


class BlogGenerator:
    """Генератор статей для блога на основе AI."""
    
    # Системный промпт для генератора статей
    SYSTEM_PROMPT = """Du bist ein erfahrener Journalist und Interior-Design-Experte, der für Hermitage Frankfurt schreibt.
Hermitage Frankfurt ist ein exklusiver Fliesen- und Innenausstattungsfachhandel in Frankfurt am Main seit 1998.

DEINE EXPERTISE:
- Fliesen aller Art (Keramik, Feinsteinzeug, Naturstein, Mosaik)
- Interior Design und Innenausstattung
- Badezimmer- und Küchengestaltung
- Aktuelle Design-Trends

DEIN SCHREIBSTIL:
- Du schreibst wie ein Mensch, nicht wie eine KI
- Natürliche, fließende Sprache mit Persönlichkeit
- Variiere Satzlänge und -struktur
- Nutze gelegentlich rhetorische Fragen
- Füge persönliche Beobachtungen oder Meinungen ein
- Vermeide Klischees und generische Phrasen
- Keine übermäßigen Aufzählungen - bevorzuge Fließtext

FIRMENKONTEXT:
- Hermitage Frankfurt - Premium Fliesen & Interior seit 1998
- Showroom: Hanauer Landstraße 421, 60314 Frankfurt
- Telefon: 069 90475570"""

    ARTICLE_PROMPT = """Schreibe einen authentischen Blog-Artikel auf Deutsch.

THEMA: {title}

QUELLENINFORMATION:
{source_context}

ANFORDERUNGEN:
- Länge: 800-1200 Wörter
- Zielgruppe: Hausbesitzer, Innenarchitekten, Bauherren in Frankfurt/Rhein-Main
- Keywords natürlich einbauen: {keywords}

STIL - SEHR WICHTIG:
- Schreibe wie ein echter Mensch, nicht wie eine KI
- Variiere die Satzanfänge (nicht immer "Die...", "Das...", "Ein...")
- Nutze Übergänge zwischen Absätzen statt harter Trennungen
- Keine horizontalen Linien (---) oder Sternchen (***) als Trenner
- Keine nummerierten Listen im Fließtext - schreibe Prosa
- Füge persönliche Einschätzungen ein ("Ich finde...", "Besonders beeindruckend...")
- Stelle gelegentlich Fragen an den Leser

STRUKTUR:
1. Einleitung: Hook, der neugierig macht (2-3 Absätze)
2. Hauptteil: 3-4 thematische Abschnitte mit H2-Überschriften (##)
   - Jeder Abschnitt hat mehrere Absätze Fließtext
   - Keine Bullet-Points, außer wenn wirklich nötig
3. Abschluss: Persönliches Fazit und Einladung in den Showroom

CALL-TO-ACTION AM ENDE:
Schließe mit einer warmherzigen Einladung in unseren Showroom (Hanauer Landstraße 421, Frankfurt).
Erwähne die Telefonnummer 069 90475570.

Schreibe NUR den Artikelinhalt, keine Meta-Informationen."""

    EXCERPT_PROMPT = """Erstelle eine kurze, ansprechende Zusammenfassung (max. 160 Zeichen) 
für folgenden Artikel. Die Zusammenfassung soll neugierig machen und zum Lesen einladen.

ARTIKEL:
{content}

Antworte NUR mit der Zusammenfassung, ohne Anführungszeichen."""

    SEO_PROMPT = """Erstelle SEO-optimierte Meta-Daten für folgenden Artikel:

TITEL: {title}
KEYWORDS: {keywords}

Antworte im Format:
SEO_TITLE: [max. 60 Zeichen, inkl. "| Hermitage Frankfurt"]
SEO_DESCRIPTION: [max. 155 Zeichen, mit Call-to-Action]

Nur diese zwei Zeilen, nichts anderes."""

    TITLE_PROMPT = """Basierend auf folgendem Trend/Thema, erstelle einen ansprechenden 
deutschen Blog-Titel für einen Fliesenfachhandel:

ORIGINAL: {original_title}
KONTEXT: {context}

Der Titel soll:
- Auf Deutsch sein
- SEO-optimiert (Keywords am Anfang)
- Maximal 70 Zeichen
- Neugierig machen
- Bezug zu Fliesen/Interior haben

Antworte NUR mit dem Titel, ohne Anführungszeichen."""

    def __init__(self):
        """Initialisiert den Blog-Generator."""
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY nicht gesetzt")
        self.client = OpenAI(api_key=api_key)
        self.model = os.environ.get('BLOG_MODEL', 'gpt-4o-mini')
    
    def generate_title_from_trend(self, trend: dict) -> str:
        """Generiert einen passenden Titel aus einem Trend."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": self.TITLE_PROMPT.format(
                    original_title=trend.get('title', ''),
                    context=trend.get('summary', '')[:500]
                )}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_content(self, title: str, keywords: list, source_context: str = ""):
        """Generiert den Artikelinhalt."""
        keywords_str = ', '.join(keywords) if isinstance(keywords, list) else keywords
        
        if not source_context:
            source_context = "Keine spezifische Quelle - allgemeines Thema"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": self.ARTICLE_PROMPT.format(
                    title=title,
                    keywords=keywords_str,
                    source_context=source_context
                )}
            ],
            max_tokens=2500,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    def generate_excerpt(self, content):
        """Generiert eine kurze Zusammenfassung."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": self.EXCERPT_PROMPT.format(content=content[:1000])}
            ],
            max_tokens=100,
            temperature=0.5,
        )
        
        excerpt = response.choices[0].message.content.strip()
        return excerpt[:160]  # Sicherheitshalber kürzen
    
    def generate_seo_meta(self, title, keywords):
        """Generiert SEO-Meta-Daten."""
        keywords_str = ', '.join(keywords) if isinstance(keywords, list) else keywords
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": self.SEO_PROMPT.format(
                    title=title,
                    keywords=keywords_str
                )}
            ],
            max_tokens=150,
            temperature=0.5,
        )
        
        result = response.choices[0].message.content
        
        # Parse response
        seo_title = ""
        seo_description = ""
        
        for line in result.split('\n'):
            if line.startswith('SEO_TITLE:'):
                seo_title = line.replace('SEO_TITLE:', '').strip()
            elif line.startswith('SEO_DESCRIPTION:'):
                seo_description = line.replace('SEO_DESCRIPTION:', '').strip()
        
        return seo_title, seo_description
    
    def create_slug(self, title):
        """Erstellt einen URL-freundlichen Slug."""
        # Versuche slugify zu verwenden, Fallback auf einfache Methode
        try:
            return slugify(title, lowercase=True, max_length=100)
        except:
            # Einfacher Fallback
            slug = title.lower()
            slug = re.sub(r'[äöü]', lambda m: {'ä': 'ae', 'ö': 'oe', 'ü': 'ue'}[m.group()], slug)
            slug = re.sub(r'[^a-z0-9]+', '-', slug)
            slug = slug.strip('-')
            return slug[:100]
    
    def generate_post(self, title, keywords, category='Trends'):
        """
        Generiert einen kompletten Blog-Artikel.
        
        Args:
            title: Titel/Thema des Artikels
            keywords: Liste von Keywords
            category: Kategorie des Artikels
        
        Returns:
            BlogPost: Der erstellte (aber nicht veröffentlichte) Artikel
        """
        # Generiere Inhalte
        content = self.generate_content(title, keywords)
        excerpt = self.generate_excerpt(content)
        seo_title, seo_description = self.generate_seo_meta(title, keywords)
        
        # Erstelle Slug
        slug = self.create_slug(title)
        
        # Prüfe ob Slug schon existiert
        existing = BlogPost.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{datetime.now().strftime('%Y%m%d')}"
        
        # Erstelle BlogPost
        post = BlogPost(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            category=category,
            tags=keywords if isinstance(keywords, list) else keywords.split(','),
            seo_title=seo_title,
            seo_description=seo_description,
            is_auto_generated=True,
            is_published=False  # Muss manuell freigegeben werden
        )
        
        db.session.add(post)
        db.session.commit()
        
        return post


class ContentScheduler:
    """Scheduler für automatische Content-Generierung."""
    
    @staticmethod
    def process_pending_plans():
        """Verarbeitet fällige Content-Pläne."""
        from app.models import ContentPlan
        
        pending = ContentPlan.get_pending()
        generator = BlogGenerator()
        
        results = []
        for plan in pending:
            try:
                plan.status = ContentPlan.STATUS_GENERATING
                db.session.commit()
                
                post = generator.generate_post(
                    title=plan.title,
                    keywords=plan.keywords,
                    category=plan.category
                )
                
                plan.blog_post = post
                plan.status = ContentPlan.STATUS_REVIEW
                db.session.commit()
                
                results.append({
                    'plan_id': plan.id,
                    'post_id': post.id,
                    'status': 'success'
                })
            except Exception as e:
                plan.status = ContentPlan.STATUS_PLANNED
                db.session.commit()
                
                results.append({
                    'plan_id': plan.id,
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    @staticmethod
    def enforce_article_limit(max_articles: int = 30):
        """
        Удаляет старые статьи, если их больше лимита.
        Сохраняет только max_articles самых новых статей.
        
        Args:
            max_articles: Максимальное количество статей для хранения
        
        Returns:
            int: Количество удалённых статей
        """
        # Считаем общее количество статей
        total_count = BlogPost.query.count()
        
        if total_count <= max_articles:
            return 0
        
        # Сколько нужно удалить
        to_delete = total_count - max_articles
        
        # Находим самые старые статьи (по дате создания)
        old_posts = BlogPost.query.order_by(
            BlogPost.created_at.asc()
        ).limit(to_delete).all()
        
        deleted_count = 0
        for post in old_posts:
            db.session.delete(post)
            deleted_count += 1
        
        db.session.commit()
        
        import logging
        logging.info(f"Удалено {deleted_count} старых статей. Осталось {max_articles}.")
        
        return deleted_count
    
    @staticmethod
    def generate_from_trends(max_articles: int = 3, auto_publish: bool = False):
        """
        Generiert Artikel basierend auf aktuellen Trends.
        
        Args:
            max_articles: Maximale Anzahl zu erstellender Artikel
            auto_publish: Wenn True, werden Artikel sofort veröffentlicht
        
        Returns:
            Liste der erstellten BlogPosts
        """
        from app.services.trends_fetcher import TrendsFetcher
        from app.services.image_fetcher import ImageFetcher
        
        fetcher = TrendsFetcher()
        generator = BlogGenerator()
        image_fetcher = ImageFetcher()
        
        # Сначала очищаем старые статьи (лимит 30)
        ContentScheduler.enforce_article_limit(max_articles=30)
        
        # Hole Trend-Themen
        topics = fetcher.get_article_topics(count=max_articles)
        
        created_posts = []
        
        for topic in topics:
            try:
                # Generiere passenden Titel
                trend_data = {
                    'title': topic['original_title'],
                    'summary': topic['summary']
                }
                title = generator.generate_title_from_trend(trend_data)
                
                # Generiere Artikel
                source_context = f"Quelle: {topic['source']}\nOriginal: {topic['original_title']}\n{topic['summary']}"
                
                content = generator.generate_content(
                    title=title,
                    keywords=topic['suggested_keywords'],
                    source_context=source_context
                )
                
                excerpt = generator.generate_excerpt(content)
                seo_title, seo_description = generator.generate_seo_meta(title, topic['suggested_keywords'])
                slug = generator.create_slug(title)
                
                # Получаем изображение для статьи
                image_data = image_fetcher.get_image_for_article(
                    title=title,
                    keywords=topic['suggested_keywords']
                )
                
                # Добавляем атрибуцию в конец контента (без разделителей)
                if image_data.get('attribution'):
                    content += f"\n\n*Titelbild: {image_data['attribution']}*"
                
                # Prüfe Duplikate
                existing = BlogPost.query.filter_by(slug=slug).first()
                if existing:
                    slug = f"{slug}-{datetime.now().strftime('%Y%m%d%H%M')}"
                
                # Erstelle Post
                post = BlogPost(
                    title=title,
                    slug=slug,
                    content=content,
                    excerpt=excerpt,
                    featured_image=image_data.get('url'),  # URL изображения
                    category='Trends',
                    tags=topic['suggested_keywords'],
                    seo_title=seo_title,
                    seo_description=seo_description,
                    is_auto_generated=True,
                    is_published=auto_publish
                )
                
                if auto_publish:
                    post.published_at = datetime.utcnow()
                
                db.session.add(post)
                db.session.commit()
                
                created_posts.append(post)
                
            except Exception as e:
                import logging
                logging.error(f"Fehler bei Trend-Artikel: {e}")
                continue
        
        # Ещё раз проверяем лимит после генерации
        ContentScheduler.enforce_article_limit(max_articles=30)
        
        return created_posts