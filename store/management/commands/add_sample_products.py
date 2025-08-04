from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from store.models import Product

class Command(BaseCommand):
    help = 'Add sample products to the database'

    def handle(self, *args, **options):
        products_data = [
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.',
                'price': 2999.00,
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop'
            },
            {
                'name': 'Smartphone - Latest Model',
                'description': 'Latest smartphone with 128GB storage, 6.7-inch display, and advanced camera system. Includes fast charging and wireless charging.',
                'price': 45999.00,
                'stock': 25,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'
            },
            {
                'name': 'Laptop - Premium Series',
                'description': 'High-performance laptop with Intel i7 processor, 16GB RAM, 512GB SSD, and 15.6-inch Full HD display. Perfect for work and gaming.',
                'price': 65999.00,
                'stock': 15,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop'
            },
            {
                'name': 'Smart Watch',
                'description': 'Feature-rich smartwatch with heart rate monitor, GPS, and 7-day battery life. Compatible with iOS and Android.',
                'price': 8999.00,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop'
            },
            {
                'name': 'Wireless Gaming Mouse',
                'description': 'High-precision gaming mouse with RGB lighting, programmable buttons, and 25K DPI sensor. Perfect for gamers.',
                'price': 3999.00,
                'stock': 40,
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop'
            },
            {
                'name': 'Mechanical Keyboard',
                'description': 'Premium mechanical keyboard with Cherry MX switches, RGB backlighting, and aluminum frame. Ideal for typing and gaming.',
                'price': 5999.00,
                'stock': 35,
                'image_url': 'https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400&h=400&fit=crop'
            },
            {
                'name': '4K Gaming Monitor',
                'description': '27-inch 4K gaming monitor with 144Hz refresh rate, 1ms response time, and HDR support. Immersive gaming experience.',
                'price': 35999.00,
                'stock': 10,
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop'
            },
            {
                'name': 'Wireless Earbuds',
                'description': 'True wireless earbuds with active noise cancellation, 24-hour battery life, and premium sound quality.',
                'price': 14999.00,
                'stock': 60,
                'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop'
            },
            {
                'name': 'Gaming Chair',
                'description': 'Ergonomic gaming chair with lumbar support, adjustable armrests, and premium fabric. Comfortable for long gaming sessions.',
                'price': 12999.00,
                'stock': 20,
                'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop'
            },
            {
                'name': 'External SSD 1TB',
                'description': 'Ultra-fast external SSD with USB 3.2 Gen 2, 1050MB/s read speed, and rugged design. Perfect for data backup.',
                'price': 7999.00,
                'stock': 45,
                'image_url': 'https://images.unsplash.com/photo-1597872200969-2b65dbfbd91f?w=400&h=400&fit=crop'
            },
            {
                'name': 'Webcam HD',
                'description': '1080p HD webcam with autofocus, built-in microphone, and privacy cover. Great for video calls and streaming.',
                'price': 3999.00,
                'stock': 55,
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop'
            },
            {
                'name': 'Wireless Charger',
                'description': 'Fast wireless charger with 15W charging speed, LED indicator, and universal compatibility.',
                'price': 1999.00,
                'stock': 70,
                'image_url': 'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=400&h=400&fit=crop'
            }
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock']
                }
            )
            
            # Add image if product was created or doesn't have an image
            if created or not product.image:
                try:
                    # Download image from URL
                    response = requests.get(product_data['image_url'], timeout=10)
                    if response.status_code == 200:
                        # Create filename
                        filename = f"{product.name.lower().replace(' ', '_')}.jpg"
                        # Save image
                        product.image.save(filename, ContentFile(response.content), save=True)
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully created product with image: {product.name}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Could not download image for: {product.name}')
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error downloading image for {product.name}: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample products have been added successfully!')
        ) 