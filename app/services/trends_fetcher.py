"""
Сервис получения трендов для генерации контента
"""

import os
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TrendsFetcher:
    """Получает трендовые темы из различных источников."""
    
    # RSS-ленты по теме ремонта, дизайна, плитки
    RSS_FEEDS = [
        # Немецкие источники
        ('https://www.schoener-wohnen.de/feed', 'Schöner Wohnen'),
        ('https://www.baulinks.de/rss/baulinks.xml', 'Baulinks'),
        ('https://www.haustechnikdialog.de/Forum/f/rss/28', 'Haustechnik'),
        # Internationale (переводим)
        ('https://www.dezeen.com/interiors/feed/', 'Dezeen Interiors'),
        ('https://www.archdaily.com/feed', 'ArchDaily'),
    ]
    
    # Ключевые слова для фильтрации
    KEYWORDS = [
        'fliesen', 'tiles', 'keramik', 'ceramic', 
        'bad', 'bathroom', 'küche', 'kitchen',
        'boden', 'floor', 'wand', 'wall',
        'design', 'interior', 'innenausstattung',
        'marmor', 'marble', 'naturstein', 'stone',
        'mosaik', 'mosaic', 'terracotta',
        'trend', 'renovation', 'renovierung',
        'sanierung', 'wellness', 'spa',
    ]
    
    def __init__(self):
        """Инициализация."""
        self.news_api_key = os.environ.get('NEWS_API_KEY')
    
    def fetch_rss_trends(self, max_items: int = 20) -> List[Dict]:
        """
        Получает тренды из RSS-лент.
        
        Returns:
            Список словарей с темами для статей
        """
        trends = []
        
        for feed_url, source_name in self.RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', entry.get('description', ''))
                    link = entry.get('link', '')
                    published = entry.get('published', '')
                    
                    # Проверяем релевантность
                    content = f"{title} {summary}".lower()
                    relevance_score = sum(1 for kw in self.KEYWORDS if kw in content)
                    
                    if relevance_score >= 2:  # Минимум 2 ключевых слова
                        trends.append({
                            'title': title,
                            'summary': summary[:500],
                            'source': source_name,
                            'url': link,
                            'published': published,
                            'relevance': relevance_score,
                            'type': 'rss'
                        })
            except Exception as e:
                logger.warning(f"Ошибка получения RSS {feed_url}: {e}")
                continue
        
        # Сортируем по релевантности
        trends.sort(key=lambda x: x['relevance'], reverse=True)
        return trends[:max_items]
    
    def fetch_google_trends(self, geo: str = 'DE') -> List[Dict]:
        """
        Получает тренды из Google Trends.
        Требует установки pytrends: pip install pytrends
        """
        try:
            from pytrends.request import TrendReq
            
            pytrends = TrendReq(hl='de-DE', tz=60)
            
            trends = []
            
            # Получаем трендовые запросы по категориям
            # Категория 11 = Home & Garden
            try:
                trending = pytrends.trending_searches(pn='germany')
                for topic in trending[0].tolist()[:10]:
                    # Проверяем релевантность
                    if any(kw in topic.lower() for kw in ['bad', 'küche', 'wohn', 'haus', 'design', 'renovier']):
                        trends.append({
                            'title': topic,
                            'summary': f"Trending topic in Germany: {topic}",
                            'source': 'Google Trends',
                            'relevance': 5,
                            'type': 'google_trends'
                        })
            except Exception as e:
                logger.warning(f"Ошибка Google Trends: {e}")
            
            # Поиск по нашим ключевым словам
            keywords_to_check = ['Fliesen Trend', 'Badezimmer Design', 'Küchenfliesen']
            
            for keyword in keywords_to_check:
                try:
                    pytrends.build_payload([keyword], timeframe='now 7-d', geo=geo)
                    related = pytrends.related_queries()
                    
                    if keyword in related and related[keyword]['rising'] is not None:
                        for _, row in related[keyword]['rising'].head(3).iterrows():
                            trends.append({
                                'title': row['query'],
                                'summary': f"Rising search trend related to {keyword}",
                                'source': 'Google Trends',
                                'relevance': 4,
                                'type': 'google_trends'
                            })
                except:
                    continue
            
            return trends
            
        except ImportError:
            logger.info("pytrends не установлен. Используйте: pip install pytrends")
            return []
        except Exception as e:
            logger.error(f"Ошибка Google Trends: {e}")
            return []
    
    def fetch_news_api(self, query: str = "Fliesen OR Badezimmer Design OR Interior Trend") -> List[Dict]:
        """
        Получает новости через News API.
        Требует NEWS_API_KEY в .env
        """
        if not self.news_api_key:
            logger.info("NEWS_API_KEY не настроен")
            return []
        
        try:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query,
                'language': 'de',
                'sortBy': 'publishedAt',
                'pageSize': 20,
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            trends = []
            for article in data.get('articles', []):
                trends.append({
                    'title': article.get('title', ''),
                    'summary': article.get('description', ''),
                    'source': article.get('source', {}).get('name', 'News API'),
                    'url': article.get('url', ''),
                    'published': article.get('publishedAt', ''),
                    'relevance': 3,
                    'type': 'news_api'
                })
            
            return trends
            
        except Exception as e:
            logger.error(f"Ошибка News API: {e}")
            return []
    
    def get_all_trends(self, max_items: int = 15) -> List[Dict]:
        """
        Получает тренды из всех источников.
        
        Returns:
            Объединённый список трендов, отсортированный по релевантности
        """
        all_trends = []
        
        # RSS (всегда работает)
        all_trends.extend(self.fetch_rss_trends())
        
        # Google Trends (если установлен pytrends)
        all_trends.extend(self.fetch_google_trends())
        
        # News API (если есть ключ)
        all_trends.extend(self.fetch_news_api())
        
        # Удаляем дубликаты по заголовку
        seen_titles = set()
        unique_trends = []
        for trend in all_trends:
            title_lower = trend['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_trends.append(trend)
        
        # Сортируем по релевантности
        unique_trends.sort(key=lambda x: x['relevance'], reverse=True)
        
        return unique_trends[:max_items]
    
    def get_article_topics(self, count: int = 5) -> List[Dict]:
        """
        Генерирует темы для статей на основе трендов.
        
        Returns:
            Список тем с предложенными ключевыми словами
        """
        trends = self.get_all_trends(max_items=count * 2)
        
        topics = []
        for trend in trends[:count]:
            # Генерируем ключевые слова для SEO
            keywords = self._extract_keywords(trend['title'], trend['summary'])
            
            topics.append({
                'original_title': trend['title'],
                'source': trend['source'],
                'summary': trend['summary'],
                'suggested_keywords': keywords,
                'relevance': trend['relevance'],
            })
        
        return topics
    
    def _extract_keywords(self, title: str, summary: str) -> List[str]:
        """Извлекает ключевые слова из текста."""
        text = f"{title} {summary}".lower()
        
        # Базовые ключевые слова для SEO
        base_keywords = ['Fliesen Frankfurt', 'Hermitage']
        
        # Добавляем релевантные ключевые слова из текста
        keyword_mapping = {
            'bad': 'Badezimmerfliesen',
            'bathroom': 'Badezimmerfliesen',
            'küche': 'Küchenfliesen',
            'kitchen': 'Küchenfliesen',
            'boden': 'Bodenfliesen',
            'floor': 'Bodenfliesen',
            'wand': 'Wandfliesen',
            'wall': 'Wandfliesen',
            'marmor': 'Marmorfliesen',
            'marble': 'Marmorfliesen',
            'naturstein': 'Naturstein',
            'mosaik': 'Mosaikfliesen',
            'design': 'Interior Design',
            'trend': 'Fliesen Trends 2025',
            'wellness': 'Wellness Bad',
            'terrace': 'Terrassenfliesen',
            'terrasse': 'Terrassenfliesen',
        }
        
        for keyword, seo_keyword in keyword_mapping.items():
            if keyword in text and seo_keyword not in base_keywords:
                base_keywords.append(seo_keyword)
        
        return base_keywords[:6]  # Макс. 6 ключевых слов
