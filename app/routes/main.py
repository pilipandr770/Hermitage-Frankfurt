"""
Основные маршруты сайта
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, send_from_directory, current_app
from app.models import Page, BlogPost
from datetime import datetime

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Главная страница."""
    page = Page.query.filter_by(slug='home').first()
    latest_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('pages/home.html', page=page, latest_posts=latest_posts)


@main_bp.route('/fliesen/')
def fliesen():
    """Страница Fliesen (Плитка)."""
    page = Page.query.filter_by(slug='fliesen').first()
    return render_template('pages/fliesen.html', page=page)


@main_bp.route('/fliesen/<city>/')
def fliesen_city(city):
    """Страницы Fliesen по городам."""
    valid_cities = ['offenbach', 'hanau', 'maintal', 'darmstadt', 'aschaffenburg']
    if city not in valid_cities:
        return render_template('errors/404.html'), 404
    
    page = Page.query.filter_by(slug=f'fliesen-{city}').first()
    return render_template('pages/fliesen_city.html', page=page, city=city)


@main_bp.route('/innenausstattung/')
def innenausstattung():
    """Страница Innenausstattung (Интерьер)."""
    page = Page.query.filter_by(slug='innenausstattung').first()
    return render_template('pages/innenausstattung.html', page=page)


@main_bp.route('/interior-design/')
def interior_design():
    """Страница Interior Design."""
    page = Page.query.filter_by(slug='interior-design').first()
    return render_template('pages/interior_design.html', page=page)


@main_bp.route('/ueber-uns/')
def about():
    """Страница Über Uns (О нас)."""
    page = Page.query.filter_by(slug='about').first()
    return render_template('pages/about.html', page=page)


@main_bp.route('/service/')
def service():
    """Страница Service."""
    page = Page.query.filter_by(slug='service').first()
    return render_template('pages/service.html', page=page)


@main_bp.route('/trends/')
def trends():
    """Страница Trends."""
    page = Page.query.filter_by(slug='trends').first()
    return render_template('pages/trends.html', page=page)


@main_bp.route('/magazine/')
def magazine():
    """Страница Magazine."""
    page = Page.query.filter_by(slug='magazine').first()
    return render_template('pages/magazine.html', page=page)


@main_bp.route('/kontakt/', methods=['GET', 'POST'])
def contact():
    """Страница контактов с формой."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # TODO: Отправка email
        # send_contact_email(name, email, phone, message)
        
        flash('Vielen Dank für Ihre Nachricht! Wir werden uns in Kürze bei Ihnen melden.', 'success')
        return redirect(url_for('main.contact'))
    
    page = Page.query.filter_by(slug='contact').first()
    return render_template('pages/contact.html', page=page)


@main_bp.route('/impressum/')
def impressum():
    """Страница Impressum."""
    page = Page.query.filter_by(slug='impressum').first()
    return render_template('pages/legal.html', page=page)


@main_bp.route('/datenschutz/')
def datenschutz():
    """Страница Datenschutzerklärung."""
    return render_template('pages/datenschutz.html')


@main_bp.route('/cookie-richtlinie/')
def cookies():
    """Страница Cookie-Richtlinie."""
    return render_template('pages/cookies.html')


@main_bp.route('/agb/')
def agb():
    """Страница AGB."""
    return render_template('pages/agb.html')


# ============ SEO & AI Files ============

@main_bp.route('/robots.txt')
def robots():
    """Robots.txt для поисковиков."""
    return send_from_directory(current_app.static_folder, 'robots.txt', mimetype='text/plain')


@main_bp.route('/llms.txt')
def llms():
    """LLMs.txt для AI-систем (ChatGPT, Claude, Gemini)."""
    return send_from_directory(current_app.static_folder, 'llms.txt', mimetype='text/plain')


@main_bp.route('/.well-known/ai-plugin.json')
def ai_plugin():
    """AI Plugin manifest для ChatGPT и других AI."""
    return send_from_directory(
        current_app.static_folder + '/.well-known', 
        'ai-plugin.json', 
        mimetype='application/json'
    )


@main_bp.route('/.well-known/security.txt')
def security_txt():
    """Security.txt."""
    return send_from_directory(
        current_app.static_folder + '/.well-known', 
        'security.txt', 
        mimetype='text/plain'
    )


@main_bp.route('/humans.txt')
def humans():
    """Humans.txt - информация о команде."""
    return send_from_directory(current_app.static_folder, 'humans.txt', mimetype='text/plain')


@main_bp.route('/sitemap.xml')
def sitemap():
    """Динамический Sitemap.xml."""
    base_url = 'https://hermitage-frankfurt.de'
    
    # Статические страницы
    static_pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'url': '/fliesen/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/innenausstattung/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/about/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/kontakt/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/service/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/trends/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/blog/', 'priority': '0.8', 'changefreq': 'daily'},
        {'url': '/impressum/', 'priority': '0.3', 'changefreq': 'yearly'},
        {'url': '/datenschutz/', 'priority': '0.3', 'changefreq': 'yearly'},
        {'url': '/agb/', 'priority': '0.3', 'changefreq': 'yearly'},
        {'url': '/cookie-richtlinie/', 'priority': '0.3', 'changefreq': 'yearly'},
    ]
    
    # Города
    cities = ['offenbach', 'hanau', 'maintal', 'darmstadt', 'aschaffenburg']
    for city in cities:
        static_pages.append({
            'url': f'/fliesen/{city}/',
            'priority': '0.7',
            'changefreq': 'monthly'
        })
    
    # Динамические страницы (блог)
    blog_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).all()
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Статические страницы
    for page in static_pages:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{page["url"]}</loc>')
        xml.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{page["priority"]}</priority>')
        xml.append('  </url>')
    
    # Блог посты
    for post in blog_posts:
        lastmod = post.updated_at or post.published_at or post.created_at
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}/blog/{post.slug}/</loc>')
        xml.append(f'    <lastmod>{lastmod.strftime("%Y-%m-%d")}</lastmod>')
        xml.append('    <changefreq>monthly</changefreq>')
        xml.append('    <priority>0.6</priority>')
        xml.append('  </url>')
    
    xml.append('</urlset>')
    
    return Response('\n'.join(xml), mimetype='application/xml')


# Обработчики ошибок
@main_bp.app_errorhandler(404)
def not_found(error):
    """Страница 404."""
    return render_template('errors/404.html'), 404


@main_bp.app_errorhandler(500)
def server_error(error):
    """Страница 500."""
    return render_template('errors/500.html'), 500
