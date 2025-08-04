from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from store.models import Product

class Command(BaseCommand):
    help = 'Fix missing images for products'

    def handle(self, *args, **options):
        # Products without images
        products_without_images = Product.objects.filter(image='')
        
        self.stdout.write(f'Found {products_without_images.count()} products without images')
        
        # Image URLs for different product types
        image_urls = {
            'ssd': 'https://images.unsplash.com/photo-1597872200969-2b65dbfbd91f?w=400&h=400&fit=crop',
            'laptop': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
            'phone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
            'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
            'watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
            'mouse': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop',
            'keyboard': 'https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400&h=400&fit=crop',
            'monitor': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop',
            'earbuds': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop',
            'chair': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop',
            'webcam': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'charger': 'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=400&h=400&fit=crop',
            'default': 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400&h=400&fit=crop'
        }
        
        for product in products_without_images:
            # Determine image type based on product name
            name_lower = product.name.lower()
            
            if 'ssd' in name_lower or 'external' in name_lower:
                image_url = image_urls['ssd']
            elif 'laptop' in name_lower:
                image_url = image_urls['laptop']
            elif 'phone' in name_lower or 'smartphone' in name_lower:
                image_url = image_urls['phone']
            elif 'headphone' in name_lower:
                image_url = image_urls['headphones']
            elif 'watch' in name_lower:
                image_url = image_urls['watch']
            elif 'mouse' in name_lower:
                image_url = image_urls['mouse']
            elif 'keyboard' in name_lower:
                image_url = image_urls['keyboard']
            elif 'monitor' in name_lower:
                image_url = image_urls['monitor']
            elif 'earbud' in name_lower:
                image_url = image_urls['earbuds']
            elif 'chair' in name_lower:
                image_url = image_urls['chair']
            elif 'webcam' in name_lower:
                image_url = image_urls['webcam']
            elif 'charger' in name_lower:
                image_url = image_urls['charger']
            else:
                image_url = image_urls['default']
            
            try:
                # Download image
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    # Create filename
                    filename = f"{product.name.lower().replace(' ', '_')}.jpg"
                    # Save image
                    product.image.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully added image for: {product.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Could not download image for: {product.name}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error downloading image for {product.name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Image fixing completed!')
        ) 