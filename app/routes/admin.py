"""
Маршруты административной панели
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Admin, ChatbotInstruction, ContentPlan, BlogPost, ChatSession

admin_bp = Blueprint('admin', __name__)


# ============ Авторизация ============

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password) and admin.is_active:
            login_user(admin)
            admin.update_last_login()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        
        flash('Ungültige Anmeldedaten', 'error')
    
    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    """Выход из системы."""
    logout_user()
    flash('Sie wurden abgemeldet.', 'info')
    return redirect(url_for('admin.login'))


# ============ Dashboard ============

@admin_bp.route('/')
@login_required
def dashboard():
    """Главная страница админки."""
    stats = {
        'blog_posts': BlogPost.query.count(),
        'published_posts': BlogPost.query.filter_by(is_published=True).count(),
        'content_plans': ContentPlan.query.filter_by(status='planned').count(),
        'chatbot_instructions': ChatbotInstruction.query.filter_by(is_active=True).count(),
        'chat_sessions': ChatSession.query.count(),
        'leads': ChatSession.query.filter_by(is_lead=True).count(),
    }
    
    # Последние лиды
    recent_leads = ChatSession.query.filter_by(is_lead=True)\
        .order_by(ChatSession.created_at.desc()).limit(5).all()
    
    # Запланированный контент
    upcoming_content = ContentPlan.query.filter_by(status='planned')\
        .order_by(ContentPlan.scheduled_date).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          stats=stats,
                          recent_leads=recent_leads,
                          upcoming_content=upcoming_content)


# ============ Инструкции чатбота ============

@admin_bp.route('/chatbot')
@login_required
def chatbot_list():
    """Список инструкций чатбота."""
    instructions = ChatbotInstruction.query.order_by(
        ChatbotInstruction.instruction_type,
        ChatbotInstruction.priority.desc()
    ).all()
    return render_template('admin/chatbot/list.html', instructions=instructions)


@admin_bp.route('/chatbot/add', methods=['GET', 'POST'])
@login_required
def chatbot_add():
    """Добавление инструкции чатбота."""
    if request.method == 'POST':
        instruction = ChatbotInstruction(
            title=request.form.get('title'),
            instruction_type=request.form.get('instruction_type'),
            content=request.form.get('content'),
            keywords=request.form.get('keywords', '').split(','),
            priority=int(request.form.get('priority', 0)),
            is_active=bool(request.form.get('is_active'))
        )
        db.session.add(instruction)
        db.session.commit()
        
        flash('Anweisung erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('admin.chatbot_list'))
    
    return render_template('admin/chatbot/form.html', instruction=None)


@admin_bp.route('/chatbot/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def chatbot_edit(id):
    """Редактирование инструкции чатбота."""
    instruction = ChatbotInstruction.query.get_or_404(id)
    
    if request.method == 'POST':
        instruction.title = request.form.get('title')
        instruction.instruction_type = request.form.get('instruction_type')
        instruction.content = request.form.get('content')
        instruction.keywords = request.form.get('keywords', '').split(',')
        instruction.priority = int(request.form.get('priority', 0))
        instruction.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        
        flash('Anweisung erfolgreich aktualisiert!', 'success')
        return redirect(url_for('admin.chatbot_list'))
    
    return render_template('admin/chatbot/form.html', instruction=instruction)


@admin_bp.route('/chatbot/delete/<int:id>', methods=['POST'])
@login_required
def chatbot_delete(id):
    """Удаление инструкции чатбота."""
    instruction = ChatbotInstruction.query.get_or_404(id)
    db.session.delete(instruction)
    db.session.commit()
    
    flash('Anweisung gelöscht.', 'info')
    return redirect(url_for('admin.chatbot_list'))


# ============ Контент-план ============

@admin_bp.route('/content-plan')
@login_required
def content_plan_list():
    """Список контент-плана."""
    plans = ContentPlan.query.order_by(ContentPlan.scheduled_date).all()
    return render_template('admin/content/list.html', plans=plans)


@admin_bp.route('/content-plan/add', methods=['GET', 'POST'])
@login_required
def content_plan_add():
    """Добавление темы в контент-план."""
    if request.method == 'POST':
        from datetime import datetime
        
        plan = ContentPlan(
            title=request.form.get('title'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            keywords=request.form.get('keywords', '').split(','),
            scheduled_date=datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%d').date(),
            status=ContentPlan.STATUS_PLANNED
        )
        db.session.add(plan)
        db.session.commit()
        
        flash('Thema zum Content-Plan hinzugefügt!', 'success')
        return redirect(url_for('admin.content_plan_list'))
    
    return render_template('admin/content/form.html', plan=None)


@admin_bp.route('/content-plan/generate/<int:id>', methods=['POST'])
@login_required
def content_plan_generate(id):
    """Генерация статьи из контент-плана."""
    plan = ContentPlan.query.get_or_404(id)
    
    # Меняем статус на "генерация"
    plan.status = ContentPlan.STATUS_GENERATING
    db.session.commit()
    
    # Запускаем генерацию
    from app.services.blog_generator import BlogGenerator
    generator = BlogGenerator()
    
    try:
        blog_post = generator.generate_post(
            title=plan.title,
            keywords=plan.keywords,
            category=plan.category
        )
        
        # Связываем с планом
        plan.blog_post = blog_post
        plan.status = ContentPlan.STATUS_REVIEW
        db.session.commit()
        
        flash('Artikel erfolgreich generiert! Bitte überprüfen.', 'success')
    except Exception as e:
        plan.status = ContentPlan.STATUS_PLANNED
        db.session.commit()
        flash(f'Fehler bei der Generierung: {str(e)}', 'error')
    
    return redirect(url_for('admin.content_plan_list'))


# ============ Блог ============

@admin_bp.route('/blog')
@login_required
def blog_list():
    """Список статей блога."""
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog/list.html', posts=posts)


@admin_bp.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def blog_edit(id):
    """Редактирование статьи блога."""
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.slug = request.form.get('slug')
        post.excerpt = request.form.get('excerpt')
        post.content = request.form.get('content')
        post.category = request.form.get('category')
        post.seo_title = request.form.get('seo_title')
        post.seo_description = request.form.get('seo_description')
        
        if request.form.get('publish') and not post.is_published:
            post.publish()
            flash('Artikel veröffentlicht!', 'success')
        
        db.session.commit()
        flash('Artikel aktualisiert!', 'success')
        return redirect(url_for('admin.blog_list'))
    
    return render_template('admin/blog/form.html', post=post)


@admin_bp.route('/blog/publish/<int:id>', methods=['POST'])
@login_required
def blog_publish(id):
    """Публикация статьи."""
    post = BlogPost.query.get_or_404(id)
    post.publish()
    
    # Обновляем статус контент-плана
    if post.content_plan:
        post.content_plan.status = ContentPlan.STATUS_PUBLISHED
    
    db.session.commit()
    
    flash('Artikel veröffentlicht!', 'success')
    return redirect(url_for('admin.blog_list'))


# ============ Лиды из чата ============

@admin_bp.route('/leads')
@login_required
def leads_list():
    """Список лидов из чата."""
    leads = ChatSession.query.filter_by(is_lead=True)\
        .order_by(ChatSession.created_at.desc()).all()
    return render_template('admin/leads/list.html', leads=leads)


@admin_bp.route('/leads/<int:id>')
@login_required
def lead_detail(id):
    """Детали лида и история чата."""
    lead = ChatSession.query.get_or_404(id)
    return render_template('admin/leads/detail.html', lead=lead)


# ============ Тренды и автогенерация ============

@admin_bp.route('/trends')
@login_required
def trends_list():
    """Показывает текущие тренды для генерации контента."""
    from app.services.trends_fetcher import TrendsFetcher
    
    fetcher = TrendsFetcher()
    trends = fetcher.get_all_trends(max_items=20)
    topics = fetcher.get_article_topics(count=10)
    
    return render_template('admin/trends/list.html', 
                          trends=trends,
                          topics=topics)


@admin_bp.route('/trends/generate', methods=['POST'])
@login_required
def trends_generate():
    """Генерирует статьи из трендов."""
    from app.services.blog_generator import ContentScheduler
    
    max_articles = int(request.form.get('max_articles', 1))
    auto_publish = bool(request.form.get('auto_publish'))
    
    try:
        posts = ContentScheduler.generate_from_trends(
            max_articles=max_articles,
            auto_publish=auto_publish
        )
        
        if posts:
            flash(f'{len(posts)} Artikel erfolgreich generiert!', 'success')
        else:
            flash('Keine passenden Trends gefunden.', 'warning')
    except Exception as e:
        flash(f'Fehler: {str(e)}', 'error')
    
    return redirect(url_for('admin.trends_list'))


@admin_bp.route('/trends/generate-single', methods=['POST'])
@login_required
def trends_generate_single():
    """Генерирует одну статью из выбранного тренда."""
    from app.services.blog_generator import BlogGenerator
    
    title = request.form.get('title')
    summary = request.form.get('summary')
    source = request.form.get('source')
    keywords = request.form.get('keywords', '').split(',')
    
    generator = BlogGenerator()
    
    try:
        # Генерируем заголовок
        trend_data = {'title': title, 'summary': summary}
        generated_title = generator.generate_title_from_trend(trend_data)
        
        # Генерируем контент
        source_context = f"Quelle: {source}\nOriginal: {title}\n{summary}"
        content = generator.generate_content(
            title=generated_title,
            keywords=[k.strip() for k in keywords if k.strip()],
            source_context=source_context
        )
        
        excerpt = generator.generate_excerpt(content)
        seo_title, seo_description = generator.generate_seo_meta(generated_title, keywords)
        slug = generator.create_slug(generated_title)
        
        # Создаём пост
        post = BlogPost(
            title=generated_title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            category='Trends',
            tags=[k.strip() for k in keywords if k.strip()],
            seo_title=seo_title,
            seo_description=seo_description,
            is_auto_generated=True,
            is_published=False
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash(f'Artikel "{generated_title}" erfolgreich generiert!', 'success')
        return redirect(url_for('admin.blog_edit', id=post.id))
        
    except Exception as e:
        flash(f'Fehler: {str(e)}', 'error')
        return redirect(url_for('admin.trends_list'))


@admin_bp.route('/blog/cleanup', methods=['POST'])
@login_required
def blog_cleanup():
    """Удаляет старые статьи, оставляя только 30 самых новых."""
    import os
    from app.services.blog_generator import ContentScheduler
    
    max_articles = int(os.environ.get('MAX_BLOG_ARTICLES', 30))
    
    try:
        deleted = ContentScheduler.enforce_article_limit(max_articles=max_articles)
        
        if deleted > 0:
            flash(f'{deleted} alte Artikel gelöscht. {max_articles} Artikel verbleiben.', 'success')
        else:
            flash(f'Keine Bereinigung erforderlich. {BlogPost.query.count()} Artikel vorhanden.', 'info')
    except Exception as e:
        flash(f'Fehler: {str(e)}', 'error')
    
    return redirect(url_for('admin.blog_list'))


@admin_bp.route('/blog/stats')
@login_required  
def blog_stats():
    """Статистика блога."""
    import os
    max_articles = int(os.environ.get('MAX_BLOG_ARTICLES', 30))
    total = BlogPost.query.count()
    published = BlogPost.query.filter_by(is_published=True).count()
    auto_generated = BlogPost.query.filter_by(is_auto_generated=True).count()
    
    return {
        'total': total,
        'published': published,
        'auto_generated': auto_generated,
        'limit': max_articles,
        'can_cleanup': total > max_articles
    }