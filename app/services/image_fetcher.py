"""
Сервис получения изображений для статей
Использует Unsplash API (бесплатно, требуется атрибуция)
"""

import os
import requests
import logging
import random
import hashlib
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class ImageFetcher:
    """Получает изображения для статей блога."""
    
    # Unsplash API (бесплатно, до 50 запросов/час)
    UNSPLASH_API = "https://api.unsplash.com/search/photos"
    
    # Расширенный маппинг ключевых слов на разные поисковые запросы
    KEYWORD_MAPPING = {
        'fliesen': ['tiles interior', 'ceramic tiles', 'floor tiles design', 'bathroom tiles'],
        'badezimmer': ['modern bathroom', 'luxury bathroom', 'bathroom interior', 'spa bathroom'],
        'küche': ['modern kitchen', 'kitchen design', 'kitchen interior', 'cooking space'],
        'marmor': ['marble texture', 'marble interior', 'marble floor', 'white marble'],
        'naturstein': ['natural stone', 'stone wall', 'stone texture', 'slate tiles'],
        'mosaik': ['mosaic tiles', 'mosaic pattern', 'tile mosaic', 'colorful mosaic'],
        'boden': ['floor design', 'flooring interior', 'hardwood floor', 'tile floor'],
        'wand': ['wall tiles', 'wall design', 'interior wall', 'textured wall'],
        'terrasse': ['terrace design', 'outdoor tiles', 'patio design', 'balcony decor'],
        'wellness': ['spa design', 'wellness interior', 'relaxation room', 'sauna design'],
        'trend': ['interior trend', 'design trend', 'modern decor', 'contemporary interior'],
        'design': ['interior design', 'home decor', 'modern design', 'minimalist interior'],
        'renovierung': ['home renovation', 'interior renovation', 'remodeling', 'home improvement'],
        'holzoptik': ['wood look', 'wood texture', 'wooden floor', 'wood interior'],
        'art deco': ['art deco interior', 'geometric pattern', 'vintage design', 'retro interior'],
        'weihnachten': ['christmas decor', 'festive interior', 'holiday home', 'winter decor'],
        'nachhaltig': ['sustainable design', 'eco interior', 'green home', 'natural materials'],
        'luxus': ['luxury interior', 'premium design', 'elegant home', 'upscale decor'],
        'modern': ['modern interior', 'contemporary home', 'minimalist design', 'clean interior'],
        'retro': ['retro interior', 'vintage decor', 'classic design', '70s style'],
    }
    
    # Fallback изображения (локальные)
    FALLBACK_IMAGES = [
        '/static/images/fliesen/grossformat.jpg',
        '/static/images/fliesen/marmor.jpg',
        '/static/images/fliesen/naturstein.jpg',
        '/static/images/fliesen/mosaic.jpg',
        '/static/images/categories/fliesen.jpg',
        '/static/images/categories/innenausstattung.jpg',
    ]
    
    def __init__(self):
        """Инициализация."""
        self.unsplash_key = os.environ.get('UNSPLASH_ACCESS_KEY')
        self.pexels_key = os.environ.get('PEXELS_API_KEY')
    
    def get_image_for_article(self, title: str, keywords: List[str]) -> Dict:
        """
        Получает подходящее изображение для статьи.
        
        Args:
            title: Заголовок статьи
            keywords: Ключевые слова
        
        Returns:
            Dict с url, author, source для атрибуции
        """
        # Пробуем Unsplash
        if self.unsplash_key:
            image = self._fetch_unsplash(title, keywords)
            if image:
                return image
        
        # Пробуем Pexels
        if self.pexels_key:
            image = self._fetch_pexels(title, keywords)
            if image:
                return image
        
        # Fallback на локальные изображения
        return self._get_fallback(keywords)
    
    def _build_search_query(self, title: str, keywords: List[str]) -> str:
        """
        Строит уникальный поисковый запрос для каждой статьи.
        Использует хеш заголовка для выбора варианта запроса.
        """
        combined_text = f"{title} {' '.join(keywords)}".lower()
        
        # Создаём хеш от заголовка для детерминированного, но разнообразного выбора
        title_hash = int(hashlib.md5(title.encode()).hexdigest(), 16)
        
        # Ищем все подходящие запросы
        matching_queries = []
        
        for keyword, search_terms in self.KEYWORD_MAPPING.items():
            if keyword in combined_text:
                matching_queries.extend(search_terms)
        
        if not matching_queries:
            # Дефолтные запросы
            matching_queries = [
                'interior design modern', 
                'home decor luxury', 
                'bathroom tiles beautiful',
                'kitchen interior design',
                'living room modern'
            ]
        
        # Выбираем запрос на основе хеша заголовка (всегда один и тот же для одного заголовка)
        selected_query = matching_queries[title_hash % len(matching_queries)]
        
        return selected_query
    
    def _get_random_photo_index(self, title: str, max_photos: int) -> int:
        """Выбирает индекс фото на основе хеша заголовка."""
        title_hash = int(hashlib.md5(title.encode()).hexdigest(), 16)
        return title_hash % max_photos
    
    def _fetch_unsplash(self, title: str, keywords: List[str]) -> Optional[Dict]:
        """Получает изображение из Unsplash."""
        try:
            query = self._build_search_query(title, keywords)
            
            response = requests.get(
                self.UNSPLASH_API,
                params={
                    'query': query,
                    'per_page': 5,
                    'orientation': 'landscape',
                },
                headers={
                    'Authorization': f'Client-ID {self.unsplash_key}'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    photo = data['results'][0]
                    return {
                        'url': photo['urls']['regular'],
                        'thumb': photo['urls']['small'],
                        'author': photo['user']['name'],
                        'author_url': photo['user']['links']['html'],
                        'source': 'Unsplash',
                        'source_url': photo['links']['html'],
                        'download_url': photo['urls']['regular'],
                        # Атрибуция для Unsplash (обязательна!)
                        'attribution': f'Foto von {photo["user"]["name"]} auf Unsplash'
                    }
            
            logger.warning(f"Unsplash API error: {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"Unsplash fetch error: {e}")
            return None
    
    def _fetch_pexels(self, title: str, keywords: List[str]) -> Optional[Dict]:
        """Получает изображение из Pexels."""
        try:
            query = self._build_search_query(title, keywords)
            
            response = requests.get(
                'https://api.pexels.com/v1/search',
                params={
                    'query': query,
                    'per_page': 15,  # Больше вариантов
                    'orientation': 'landscape',
                },
                headers={
                    'Authorization': self.pexels_key
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('photos') and len(data['photos']) > 0:
                    # Выбираем фото на основе хеша заголовка (разное для каждой статьи)
                    photo_index = self._get_random_photo_index(title, len(data['photos']))
                    photo = data['photos'][photo_index]
                    return {
                        'url': photo['src']['large'],
                        'thumb': photo['src']['medium'],
                        'author': photo['photographer'],
                        'author_url': photo['photographer_url'],
                        'source': 'Pexels',
                        'source_url': photo['url'],
                        'download_url': photo['src']['original'],
                        'attribution': f'Foto von {photo["photographer"]} auf Pexels'
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Pexels fetch error: {e}")
            return None
    
    def _get_fallback(self, keywords: List[str]) -> Dict:
        """Возвращает локальное изображение как fallback."""
        # Выбираем изображение на основе ключевых слов
        combined = ' '.join(keywords).lower()
        
        if 'bad' in combined or 'bathroom' in combined:
            img = '/static/images/innenausstattung/bathroom.jpg'
        elif 'küche' in combined or 'kitchen' in combined:
            img = '/static/images/fliesen/subway-tiles.jpg'
        elif 'marmor' in combined or 'marble' in combined:
            img = '/static/images/fliesen/marmor.jpg'
        elif 'naturstein' in combined or 'stone' in combined:
            img = '/static/images/fliesen/naturstein.jpg'
        elif 'mosaik' in combined or 'mosaic' in combined:
            img = '/static/images/fliesen/mosaic.jpg'
        else:
            img = '/static/images/fliesen/grossformat.jpg'
        
        return {
            'url': img,
            'thumb': img,
            'author': 'Hermitage Frankfurt',
            'source': 'Lokal',
            'attribution': None  # Не нужна для своих фото
        }
    
    def download_image(self, url: str, save_path: str) -> bool:
        """
        Скачивает изображение и сохраняет локально.
        
        Args:
            url: URL изображения
            save_path: Путь для сохранения
        
        Returns:
            True если успешно
        """
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            logger.error(f"Image download error: {e}")
            return False
