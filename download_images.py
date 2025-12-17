"""
Скрипт для скачивания изображений с оригинального сайта hermitage-frankfurt.de
"""

import os
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time

# Базовый URL
BASE_URL = "https://hermitage-frankfurt.de"

# Папка для сохранения
SAVE_DIR = "app/static/images/downloaded"

# Страницы для парсинга
PAGES = [
    "/",
    "/fliesen/",
    "/innenausstattung/",
    "/about/",
    "/service-new/",
    "/trends/",
    "/kontakt/",
    "/interior-design/",
    "/fliesen-offenbach/",
    "/fliesen-hanau/",
    "/fliesen-maintal/",
    "/fliesen-darmstadt/",
    "/fliesen-aschaffenburg/",
]

# Заголовки для запросов
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_all_images(url):
    """Получить все URL изображений со страницы."""
    images = set()
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем img теги
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                full_url = urljoin(url, src)
                if 'hermitage-frankfurt.de' in full_url:
                    images.add(full_url)
            
            # srcset
            srcset = img.get('srcset')
            if srcset:
                for src_item in srcset.split(','):
                    src_url = src_item.strip().split(' ')[0]
                    if src_url:
                        full_url = urljoin(url, src_url)
                        if 'hermitage-frankfurt.de' in full_url:
                            images.add(full_url)
        
        # Ищем background-image в style
        for tag in soup.find_all(style=True):
            style = tag.get('style', '')
            urls = re.findall(r'url\(["\']?([^"\'()]+)["\']?\)', style)
            for bg_url in urls:
                full_url = urljoin(url, bg_url)
                if 'hermitage-frankfurt.de' in full_url:
                    images.add(full_url)
        
        # Ищем в CSS внутри style тегов
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                urls = re.findall(r'url\(["\']?([^"\'()]+)["\']?\)', style_tag.string)
                for bg_url in urls:
                    full_url = urljoin(url, bg_url)
                    if 'hermitage-frankfurt.de' in full_url:
                        images.add(full_url)
        
        # Ищем video и source теги
        for video in soup.find_all(['video', 'source']):
            src = video.get('src')
            if src:
                full_url = urljoin(url, src)
                if 'hermitage-frankfurt.de' in full_url:
                    images.add(full_url)
        
        # Ищем ссылки на изображения
        for a in soup.find_all('a', href=True):
            href = a['href']
            if any(ext in href.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.webm']):
                full_url = urljoin(url, href)
                if 'hermitage-frankfurt.de' in full_url:
                    images.add(full_url)
        
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
    
    return images


def download_image(url, save_dir):
    """Скачать изображение."""
    try:
        # Получаем имя файла
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename:
            return None
        
        # Создаём подпапку на основе пути
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) > 1:
            subdir = os.path.join(save_dir, *path_parts[:-1])
        else:
            subdir = save_dir
        
        os.makedirs(subdir, exist_ok=True)
        filepath = os.path.join(subdir, filename)
        
        # Пропускаем если уже скачано
        if os.path.exists(filepath):
            print(f"Уже существует: {filename}")
            return filepath
        
        # Скачиваем
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Скачано: {filename}")
        return filepath
        
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return None


def main():
    """Основная функция."""
    print("=" * 60)
    print("Скачивание изображений с hermitage-frankfurt.de")
    print("=" * 60)
    
    # Создаём папку
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    all_images = set()
    
    # Собираем изображения со всех страниц
    for page in PAGES:
        url = urljoin(BASE_URL, page)
        print(f"\nПарсинг: {url}")
        images = get_all_images(url)
        print(f"  Найдено: {len(images)} изображений")
        all_images.update(images)
        time.sleep(0.5)  # Пауза между запросами
    
    print(f"\n{'=' * 60}")
    print(f"Всего уникальных изображений: {len(all_images)}")
    print("=" * 60)
    
    # Фильтруем только нужные форматы
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.mp4', '.webm')
    filtered_images = [img for img in all_images if any(img.lower().endswith(ext) for ext in valid_extensions)]
    
    print(f"После фильтрации: {len(filtered_images)}")
    
    # Скачиваем
    downloaded = 0
    for i, img_url in enumerate(sorted(filtered_images), 1):
        print(f"\n[{i}/{len(filtered_images)}] ", end="")
        result = download_image(img_url, SAVE_DIR)
        if result:
            downloaded += 1
        time.sleep(0.3)
    
    print(f"\n{'=' * 60}")
    print(f"Скачано файлов: {downloaded}")
    print(f"Сохранено в: {os.path.abspath(SAVE_DIR)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
