"""
Оптимізація hero зображень без зміни якості візуально
"""
from PIL import Image
import os

# Директорія з зображеннями
hero_dir = 'app/static/images/hero'

# Зображення для оптимізації
images_to_optimize = [
    ('slide-2.png', 'slide-2.jpg', 80),  # Конвертуємо PNG в JPG
    ('slide-3.jpg', 'slide-3.jpg', 75),
    ('slide-4.png', 'slide-4.jpg', 80),  # Конвертуємо PNG в JPG
    ('slide-5.png', 'slide-5.jpg', 80),  # Конвертуємо PNG в JPG
]

print("🖼️  Оптимізація hero зображень...")
print("=" * 60)

total_saved = 0

for input_name, output_name, quality in images_to_optimize:
    input_path = os.path.join(hero_dir, input_name)
    output_path = os.path.join(hero_dir, output_name)
    
    if not os.path.exists(input_path):
        print(f"⚠️  {input_name} не знайдено")
        continue
    
    try:
        # Відкриваємо зображення
        img = Image.open(input_path)
        
        # Якщо PNG з прозорістю, конвертуємо в RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            # Створюємо білий фон
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Ресайз якщо більше 1920px
        max_width = 1920
        if img.size[0] > max_width:
            aspect_ratio = img.size[1] / img.size[0]
            new_height = int(max_width * aspect_ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"  📐 Resize: {img.size[0]}x{img.size[1]}")
        
        # Зберігаємо як оптимізований JPG
        img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
        
        # Статистика
        original_size = os.path.getsize(input_path) / 1024  # KB
        new_size = os.path.getsize(output_path) / 1024
        saved = original_size - new_size
        savings_percent = (saved / original_size) * 100
        total_saved += saved
        
        print(f"✅ {input_name} → {output_name}")
        print(f"   {original_size:.1f} KB → {new_size:.1f} KB")
        print(f"   Економія: {saved:.1f} KB ({savings_percent:.1f}%)")
        print()
        
    except Exception as e:
        print(f"❌ Помилка при обробці {input_name}: {e}")
        print()

print("=" * 60)
print(f"💾 Загальна економія: {total_saved:.1f} KB ({total_saved/1024:.1f} MB)")
print("✅ Оптимізація завершена!")
