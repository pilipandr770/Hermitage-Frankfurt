"""
Маршруты блога
"""

from flask import Blueprint, render_template, request, abort
from app.models import BlogPost

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """Список статей блога."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    posts = BlogPost.get_published().paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    categories = ['Trends', 'Tipps', 'Projekte', 'News']
    
    return render_template('blog/index.html', 
                          posts=posts, 
                          categories=categories)


@blog_bp.route('/<slug>/')
def post(slug):
    """Отдельная статья блога."""
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Увеличиваем счётчик просмотров
    post.increment_views()
    from app import db
    db.session.commit()
    
    # Похожие статьи
    related = BlogPost.query.filter(
        BlogPost.is_published == True,
        BlogPost.category == post.category,
        BlogPost.id != post.id
    ).limit(3).all()
    
    return render_template('blog/post.html', post=post, related=related)


@blog_bp.route('/kategorie/<category>/')
def category(category):
    """Статьи по категории."""
    page = request.args.get('page', 1, type=int)
    
    posts = BlogPost.get_by_category(category).paginate(
        page=page,
        per_page=10,
        error_out=False
    )
    
    if not posts.items and page > 1:
        abort(404)
    
    return render_template('blog/category.html', 
                          posts=posts, 
                          category=category)
