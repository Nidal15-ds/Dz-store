from django.core.management.base import BaseCommand
from store.models import Category, Product, Wilaya

CATEGORIES = [
    ('Qamiss', 'qamiss'),
    ('Sport Shoes', 'sport-shoes'),
    ('T-Shirts', 't-shirts'),
    ('Watches', 'watches'),
    ('Jackets', 'jackets'),
    ('Slacks', 'slacks'),
    ('Packs (Bundles)', 'packs-bundles'),
]

WILAYAS = [
    (1, 'Adrar'), (2, 'Chlef'), (3, 'Laghouat'), (4, 'Oum El Bouaghi'),
    (5, 'Batna'), (6, 'Béjaïa'), (7, 'Biskra'), (8, 'Béchar'), (9, 'Blida'),
    (10, 'Bouira'), (11, 'Tamanrasset'), (12, 'Tébessa'), (13, 'Tlemcen'),
    (14, 'Tiaret'), (15, 'Tizi Ouzou'), (16, 'Alger'), (17, 'Djelfa'),
    (18, 'Jijel'), (19, 'Sétif'), (20, 'Saïda'), (21, 'Skikda'),
    (22, 'Sidi Bel Abbès'), (23, 'Annaba'), (24, 'Guelma'), (25, 'Constantine'),
    (26, 'Médéa'), (27, 'Mostaganem'), (28, "M'Sila"), (29, 'Mascara'),
    (30, 'Ouargla'), (31, 'Oran'), (32, 'El Bayadh'), (33, 'Illizi'),
    (34, 'Bordj Bou Arréridj'), (35, 'Boumerdès'), (36, 'El Tarf'),
    (37, 'Tindouf'), (38, 'Tissemsilt'), (39, 'El Oued'), (40, 'Khenchela'),
    (41, 'Souk Ahras'), (42, 'Tipaza'), (43, 'Mila'), (44, 'Aïn Defla'),
    (45, 'Naâma'), (46, 'Aïn Témouchent'), (47, 'Ghardaïa'), (48, 'Relizane'),
    (49, 'Timimoun'), (50, 'Bordj Badji Mokhtar'), (51, 'Ouled Djellal'),
    (52, 'Béni Abbès'), (53, 'In Salah'), (54, 'In Guezzam'), (55, 'Touggourt'),
    (56, 'Djanet'), (57, "El M'Ghair"), (58, 'El Meniaa'),
]

# (name, category, price, rating, image_url, description, is_pack)
PRODUCTS = [
    ("Mens Steel Grey Qatari Thobe", "Qamiss", 4500, 4.8,
     "https://mylittlejubba.com/cdn/shop/files/mens_latte_kuwaiti_thobe_qamees_for_men_jubba_mens_thobe_kandura3_64e2668b-2fa2-4298-a787-5c978950c5d0_1800x1800.png?v=1725489128",
     "Premium steel grey Qatari thobe featuring a clean mandarin collar and structured folding finish.", False),
    ("Mens Ready Made Golden Kuwaiti Thobe", "Qamiss", 5200, 4.9,
     "https://mylittlejubba.com/cdn/shop/files/ARMYGREENBAHRAINITHOBE_JUBBAFORMEN_QAMEESKONDURA_6_c84b292f-e3be-4bcf-9184-0b47c238ecde_1800x1800.png?v=1725489058",
     "Sophisticated Kuwaiti thobe crafted from premium white fabric with fine front button detailing.", False),
    ("Mens Emerald Green Emirati Thobe", "Qamiss", 4800, 4.7,
     "https://mylittlejubba.com/cdn/shop/files/Mens_two_tone_Thobe_with_caramel_Embroidery_Full_Set_7-258355_1800x1800.png?v=1727045897",
     "Elegant emerald green Emirati thobe with traditional loop button placket and collar stitching.", False),
    ("Mens Cream Saudi Thobe with Gold Embroidery", "Qamiss", 6500, 5.0,
     "https://mylittlejubba.com/cdn/shop/files/MensNavySaudiThobeLuxuryPolyester2_1800x1800.jpg?v=1765975410",
     "Luxurious cream Saudi thobe featuring rich traditional chest and placket gold embroidery work.", False),
    ("Urban Runner Pro Sneakers", "Sport Shoes", 6500, 4.8,
     "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
     "High-performance athletic sneakers featuring breathable mesh and shock-absorbing soles for active daily movement.", False),
    ("Streetwear Flex Sport Shoes", "Sport Shoes", 5900, 4.5,
     "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80",
     "Stylish everyday sports shoes combining modern aesthetics with maximum arch support and durability.", False),
    ("Elite Training Gym Sneakers", "Sport Shoes", 7200, 4.9,
     "https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&w=800&q=80",
     "Engineered for intense workouts and running tracks with reinforced grip and ultra-lightweight construction.", False),
    ("Classic White Court Kicks", "Sport Shoes", 5500, 4.7,
     "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=800&q=80",
     "Clean minimalist white sport shoes that effortlessly match both casual jeans and tracksuits.", False),
    ("Minimalist Heavyweight Cotton Tee", "T-Shirts", 2200, 4.6,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeeZeScJHnHG2wQeOMx_XZV7W57KlPH9DEwUJZR7ypXU9GJFM8inZIvTFB&s=10",
     "Premium 100% combed cotton t-shirt with a structured fit that holds its shape wash after wash.", False),
    ("Urban Streetwear Graphic T-Shirt", "T-Shirts", 2500, 4.4,
     "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?auto=format&fit=crop&w=800&q=80",
     "Modern oversized fit t-shirt featuring subtle chest typography and ultra-soft fabric.", False),
    ("Basic Olive Green Crewneck Tee", "T-Shirts", 2000, 4.7,
     "https://www.trueclassictees.com/cdn/shop/files/4000_MILITARYGREEN_1_hh9xue.jpg?v=1762562179",
     "Versatile everyday crewneck tee in a rich olive tone, designed for breathable all-day comfort.", False),
    ("Jet Black Slim Fit T-Shirt", "T-Shirts", 2100, 4.8,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfy8Pbl8jVymWOFI9pyIy5_2Rhs_5pTueROkRb5JRavw&s=10",
     "Essential black slim-fit t-shirt crafted with fade-resistant dye and stretch cotton.", False),
    ("Chronograph Steel Executive Watch", "Watches", 8500, 4.9,
     "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
     "Stunning stainless steel watch with a deep black dial, precise quartz movement, and premium metal strap.", False),
    ("Minimalist Leather Strap Timepiece", "Watches", 6800, 4.7,
     "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=800&q=80",
     "Classic brown genuine leather watch face design that pairs exceptionally well with traditional and formal wear.", False),
    ("Sport Tactical Digital Watch", "Watches", 5400, 4.6,
     "https://images.unsplash.com/photo-1533139502658-0198f920d8e8?auto=format&fit=crop&w=800&q=80",
     "Rugged waterproof digital watch built for outdoor activities, training, and heavy daily usage.", False),
    ("All-Black Matte Chronograph", "Watches", 9200, 4.9,
     "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?auto=format&fit=crop&w=800&q=80",
     "Bold matte-finish black timepiece featuring scratch-resistant mineral glass and luxury aesthetic.", False),
    ("Classic Black Leather Biker Jacket", "Jackets", 12000, 4.9,
     "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80",
     "Premium faux-leather biker jacket with robust metal zips and a sharp tailored cut.", False),
    ("Urban Bomber Jacket", "Jackets", 9500, 4.7,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ003Ecqo8sFNSOPc_lZQEd_1OzL7jzOU6o0MdHzC8mRA&s=10",
     "Lightweight windproof bomber jacket equipped with ribbed cuffs and utility arm pocket.", False),
    ("Rugged Denim Trucker Jacket", "Jackets", 8500, 4.6,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgRyYq_YC81KKZaNL8aBYUm1qnRDKMshuHSAMumVgzVY6yxYo6aB2k5FbT&s=10",
     "Vintage-washed blue denim jacket featuring durable stitching and timeless casual styling.", False),
    ("All-Weather Hooded Windbreaker", "Jackets", 7800, 4.8,
     "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=800&q=80",
     "Water-resistant windbreaker jacket designed to keep you warm and dry during transitional seasons.", False),
    ("Tailored Slim-Fit Formal Slacks", "Slacks", 4900, 4.7,
     "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80",
     "Crisp formal trousers tailored with wrinkle-resistant fabric for professional and dressy occasions.", False),
    ("Casual Cotton Chino Pants", "Slacks", 4500, 4.6,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJGAZlDP9bIK5jy7BefguBTGuMA51dEXMLA491i3czEQ&s=10",
     "Versatile stretch-cotton chinos providing exceptional comfort and a clean modern silhouette.", False),
    ("Pleated Smart-Casual Trousers", "Slacks", 5200, 4.8,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRg3-Fyih_15k4fOiAd9bwYQ0sb2Nwojg9QMn1mA2RiNA&s=10",
     "Relaxed yet sharp pleated trousers designed for contemporary streetwear and smart-casual looks.", False),
    ("Dark Grey Urban Cargo Slacks", "Slacks", 5600, 4.7,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTT_4q0bxGmLgg9wVf6749pw84pa-Djm5k-XVPTmJowEQ&s=10",
     "Functional dark grey trousers with deep utility pockets and durable twill fabric.", False),
    ("The Ultimate Gentleman Qamiss Pack", "Packs (Bundles)", 9500, 5.0,
     "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=800&q=80",
     "Includes 1 Premium White Qamiss, 1 Leather Strap Watch, and 1 matching prayer cap at a 15% discount.", True),
    ("Streetwear Summer Bundle", "Packs (Bundles)", 7800, 4.9,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0kam5feOv6rQYZNeQavm6NoA4ENMfUhZVtMFX5L1JIA&s=10",
     "Includes 2 Heavyweight Cotton T-Shirts and 1 pair of Urban Runner Sport Shoes packaged together.", True),
    ("Complete Executive Outfit Pack", "Packs (Bundles)", 13500, 4.9,
     "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80",
     "Includes 1 Tailored Slim-Fit Slack, 1 Premium Button Tee, and 1 Steel Chronograph Watch.", True),
    ("Active Sport & Watch Combo Pack", "Packs (Bundles)", 11000, 4.8,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4fFjD0W6e-kM2cD6zpjWYlgC49APyJDPrL-TCbbKaig&s=10",
     "Includes 1 pair of Elite Gym Sneakers and 1 Sport Tactical Digital Watch for maximum performance value.", True),
]


class Command(BaseCommand):
    help = 'Seed categories, 58 wilayas and 28 demo products'

    def handle(self, *args, **options):
        for name, slug in CATEGORIES:
            Category.objects.get_or_create(name=name, defaults={'slug': slug})

        for code, name in WILAYAS:
            Wilaya.objects.get_or_create(code=code, defaults={'name': name})

        for name, cat, price, rating, image, desc, is_pack in PRODUCTS:
            category = Category.objects.get(name=cat)
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'price': price,
                    'stock': 10,
                    'rating': rating,
                    'image_url': image,
                    'description': desc,
                    'is_pack': is_pack,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seed done: {Category.objects.count()} categories, "
            f"{Wilaya.objects.count()} wilayas, {Product.objects.count()} products."
        ))