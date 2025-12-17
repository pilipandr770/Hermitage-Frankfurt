"""
Скрипт для организации скачанных изображений в структуру проекта
"""

import os
import shutil
from pathlib import Path

# Исходная папка с загрузками
SOURCE_DIR = Path("app/static/images/downloaded/wp-content/uploads")

# Целевая папка
TARGET_DIR = Path("app/static/images")

# Маппинг файлов к категориям
FILE_MAPPING = {
    # Logo
    "logo_new.png": "logo.png",
    
    # Hero images
    "GANZ-OBEN-BEI-FLIESEN-1500x630.jpg": "hero/fliesen-hero.jpg",
    "innenausstattung-1076x430.png": "hero/innenausstattung-hero.jpg", 
    "Galleria-Concept_32-1500x430.jpg": "hero/hero-bg.jpg",
    "future-1500x430.jpg": "hero/trends-hero.jpg",
    "individual-1500x430.png": "hero/service-hero.jpg",
    "kontakt.png": "hero/contact-hero.jpg",
    "back-new-1500x430.png": "hero/about-hero.jpg",
    
    # Categories
    "fliesen.png": "categories/fliesen.jpg",
    "innen.png": "categories/innenausstattung.jpg",
    "interior-design.png": "categories/interior-design.jpg",
    "trends.png": "categories/trends.jpg",
    
    # Showroom / About
    "4S3A0002.jpg": "showroom.jpg",
    "4S3A0134.jpg": "showroom-2.jpg",
    "4S3A0202.jpg": "showroom-3.jpg",
    "dasisthermitage.png": "about-hermitage.jpg",
    "Pavilion1-AG7G_tm-705x423.jpg": "showroom-about.jpg",
    
    # Gallery - Interior
    "4S3A4410.jpg": "gallery/interior-1.jpg",
    "4S3A4455.jpg": "gallery/interior-2.jpg",
    "4S3A4481.jpg": "gallery/interior-3.jpg",
    "4S3A4496.jpg": "gallery/interior-4.jpg",
    "4S3A4558.jpg": "gallery/interior-5.jpg",
    "4S3A4566.jpg": "gallery/interior-6.jpg",
    "4S3A4607.jpg": "gallery/interior-7.jpg",
    "4S3A4640.jpg": "gallery/interior-8.jpg",
    "4S3A4667.jpg": "gallery/interior-9.jpg",
    
    # Gallery - Showroom
    "4S3A8117.jpg": "gallery/showroom-1.jpg",
    "4S3A8308.jpg": "gallery/showroom-2.jpg",
    "4S3A8370.jpg": "gallery/showroom-3.jpg",
    "4S3A8378.jpg": "gallery/showroom-4.jpg",
    "4S3A8380.jpg": "gallery/showroom-5.jpg",
    "4S3A8621.jpg": "gallery/showroom-6.jpg",
    
    # Gallery - Products
    "4S3A8983.jpg": "gallery/products-1.jpg",
    "4S3A9081.jpg": "gallery/products-2.jpg",
    "4S3A9084.jpg": "gallery/products-3.jpg",
    "4S3A9093.jpg": "gallery/products-4.jpg",
    "4S3A9510.jpg": "gallery/products-5.jpg",
    "4S3A9525.jpg": "gallery/products-6.jpg",
    "4S3A9688.jpg": "gallery/products-7.jpg",
    "4S3A9690.jpg": "gallery/products-8.jpg",
    "4S3A9818.jpg": "gallery/products-9.jpg",
    "4S3A9829.jpg": "gallery/products-10.jpg",
    "4S3A9835.jpg": "gallery/products-11.jpg",
    "4S3A9993.jpg": "gallery/products-12.jpg",
    
    # Fliesen types
    "basic_fliesen01-1200x630.jpg": "fliesen/fliesen-main.jpg",
    "brick-02-705x564.jpg": "fliesen/brick.jpg",
    "mosaic-05-705x564.jpg": "fliesen/mosaic.jpg",
    "wood-01-705x564.jpg": "fliesen/wood.jpg",
    "outdoor-705x499.png": "fliesen/outdoor.jpg",
    "oben-2_marmor-705x499.jpg": "fliesen/marmor.jpg",
    "oben1-705x564.jpg": "fliesen/naturstein.jpg",
    "Galleria-Concept_24-845x684.jpg": "fliesen/grossformat.jpg",
    "Galleria_Slabs_2-845x684.jpg": "fliesen/slabs.jpg",
    "Caprice-Provence-y-Base-Black-20x20-1024x725-705x499.jpg": "fliesen/caprice.jpg",
    "gaudi_MG_5551_1-463x705.jpg": "fliesen/gaudi.jpg",
    
    # Innenausstattung
    "Krukje-705x497.jpg": "innenausstattung/furniture-1.jpg",
    "Puro_with_plinth_RS-1-705x649.jpg": "innenausstattung/furniture-2.jpg",
    "Visionnaire05-705x402.png": "innenausstattung/visionnaire.jpg",
    "booma05-705x538.png": "innenausstattung/lighting.jpg",
    "sv08-705x490.png": "innenausstattung/bathroom.jpg",
    "rivera02.png": "innenausstattung/textiles.jpg",
    
    # Villa projects
    "vill_1.jpg": "projects/villa-1.jpg",
    "vill_2.jpg": "projects/villa-2.jpg",
    "vill_3.jpg": "projects/villa-3.jpg",
    "vill_4.jpg": "projects/villa-4.jpg",
    "franz_4-1.jpg": "projects/project-1.jpg",
    "IMG_0152-e1547683229770-495x400.jpg": "projects/project-2.jpg",
    "IMG_4117-495x400.jpg": "projects/project-3.jpg",
    "IMG_8143_sm-495x400.jpg": "projects/project-4.jpg",
    "IMG_8809-495x400.jpg": "projects/project-5.jpg",
    "PHOTO-2018-11-22-10-02-13-705x529.jpg": "projects/project-6.jpg",
    
    # Brands
    "aparici.png": "brands/aparici.png",
    "casalgrande.png": "brands/casalgrande.png",
    "gardenia.png": "brands/gardenia.png",
    "saloni.png": "brands/saloni.png",
    "casear.png": "brands/casear.png",
    "ital.png": "brands/ital.png",
    "laufen.png": "brands/laufen.png",
    "osborne.png": "brands/osborne.png",
    "tau.png": "brands/tau.png",
    "versac.png": "brands/versac.png",
    "vives.png": "brands/vives.png",
    
    # Icons/Other
    "01.png": "icons/icon-1.png",
    "02.png": "icons/icon-2.png",
    "03.png": "icons/icon-3.png",
    "04.png": "icons/icon-4.png",
    "04-Kopie.png": "icons/icon-5.png",
    "our-tile-495x104.png": "banners/our-tile.png",
    "all-you-need.png": "banners/all-you-need.png",
    "we_love_tiles.png": "banners/we-love-tiles.png",
    "text.png": "banners/text.png",
    "mag1.png": "magazine/mag-1.png",
    "indi.png": "banners/individual.png",
    "start-705x487.jpg": "misc/start.jpg",
    "start-705x506.png": "misc/start-2.png",
    "oben-569x705.png": "misc/oben.png",
    "oben-705x530.jpg": "misc/oben-2.jpg",
    "garganti02-1304x430.png": "misc/garganti.png",
    "white-bevelled-subway-tiles-tiles-flooring-western-distributors-bevelled-subway-tile-222-1-1400x630.png": "fliesen/subway-tiles.jpg",
    "Bildschirmfoto-2019-03-05-um-17.18.33-563x705.png": "misc/screenshot.png",
}


def find_file(filename, source_dir):
    """Рекурсивный поиск файла."""
    for root, dirs, files in os.walk(source_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None


def organize_images():
    """Организация изображений."""
    print("=" * 60)
    print("Организация изображений")
    print("=" * 60)
    
    copied = 0
    errors = []
    
    for src_name, dst_path in FILE_MAPPING.items():
        src_file = find_file(src_name, SOURCE_DIR)
        
        if src_file:
            dst_file = TARGET_DIR / dst_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(src_file, dst_file)
                print(f"✓ {src_name} → {dst_path}")
                copied += 1
            except Exception as e:
                errors.append(f"{src_name}: {e}")
        else:
            errors.append(f"{src_name}: не найден")
    
    print(f"\n{'=' * 60}")
    print(f"Скопировано: {copied} файлов")
    
    if errors:
        print(f"\nОшибки ({len(errors)}):")
        for err in errors[:10]:
            print(f"  - {err}")
    
    print("=" * 60)


if __name__ == "__main__":
    organize_images()
