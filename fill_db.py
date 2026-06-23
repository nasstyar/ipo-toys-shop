import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Manufacturer, Category, Product, Cart, CartItem

# Очистка старых данных
CartItem.objects.all().delete()
Cart.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()
Manufacturer.objects.all().delete()
User.objects.filter(username__startswith='user').delete()

print("Старые данные удалены")

# === 1. Производители (5 шт.) ===
manufacturers = [
    Manufacturer.objects.create(name="LEGO", country="Дания", description="Конструкторы"),
    Manufacturer.objects.create(name="Mattel", country="США", description="Игрушки Barbie"),
    Manufacturer.objects.create(name="Hasbro", country="США", description="Игрушки и игры"),
    Manufacturer.objects.create(name="Playmobil", country="Германия", description="Фигурки"),
    Manufacturer.objects.create(name="Fisher-Price", country="США", description="Игрушки для малышей"),
]
print(f"Создано производителей: {len(manufacturers)}")

# === 2. Категории (10 шт.) ===
categories = [
    Category.objects.create(name="Конструкторы", description="LEGO и аналоги"),
    Category.objects.create(name="Куклы", description="Куклы и аксессуары"),
    Category.objects.create(name="Машинки", description="Игрушечные автомобили"),
    Category.objects.create(name="Настольные игры", description="Игры для семьи"),
    Category.objects.create(name="Плюшевые игрушки", description="Мягкие игрушки"),
    Category.objects.create(name="Развивающие игрушки", description="Для дошкольников"),
    Category.objects.create(name="Фигурки", description="Playmobil и другие"),
    Category.objects.create(name="Оружие", description="Игрушечное оружие"),
    Category.objects.create(name="Творчество", description="Наборы для творчества"),
    Category.objects.create(name="Для малышей", description="Игрушки 0-3 года"),
]
print(f"Создано категорий: {len(categories)}")

# === 3. Товары (34 шт.) ===
products_data = [
    ("LEGO City Полицейский участок", "Большой набор LEGO", 89.99, 15, 0, 0),
    ("Barbie Кукла", "Классическая кукла Barbie", 24.99, 30, 1, 1),
    ("LEGO Friends Дом", "Дом для кукол LEGO", 129.99, 10, 0, 0),
    ("Hot Wheels Трек", "Гоночный трек с машинками", 34.99, 25, 2, 2),
    ("Monopoly Классическая", "Настольная игра", 29.99, 20, 3, 2),
    ("Плюшевый мишка", "Большой медведь 50см", 39.99, 18, 4, 4),
    ("LEGO Star Wars", "Набор Star Wars", 79.99, 12, 0, 0),
    ("Barbie Дом мечты", "Большой дом для Barbie", 199.99, 5, 1, 1),
    ("Playmobil Замок", "Средневековый замок", 89.99, 8, 6, 3),
    ("Машинка на пульте", "Радиоуправляемая машина", 49.99, 22, 2, 2),
    ("LEGO Technic", "Сложный конструктор", 149.99, 7, 0, 0),
    ("Кукла LOL Surprise", "Кукла с сюрпризом", 19.99, 40, 1, 1),
    ("Ниндзяго набор", "LEGO Ninjago", 59.99, 14, 0, 0),
    ("Мяч футбольный", "Детский футбольный мяч", 14.99, 50, 7, 4),
    ("Пазл 1000 деталей", "Большой пазл", 16.99, 35, 8, 4),
    ("LEGO Harry Potter", "Набор Hogwarts", 99.99, 9, 0, 0),
    ("Barbie Машина", "Розовый кабриолет", 29.99, 25, 1, 1),
    ("Playmobil Ферма", "Набор фермы", 69.99, 11, 6, 3),
    ("Конструктор магнитный", "Magformers 50 деталей", 54.99, 16, 5, 4),
    ("Мягкая игрушка заяц", "Плюшевый заяц", 24.99, 30, 4, 4),
    ("LEGO Duplo Паровоз", "Для малышей", 44.99, 20, 9, 4),
    ("Barbie Щенки", "Игрушка с питомцами", 34.99, 22, 1, 1),
    ("Машинка инерционная", "Набор из 5 машинок", 19.99, 45, 2, 2),
    ("Настольная игра Уно", "Карточная игра", 12.99, 60, 3, 2),
    ("LEGO Minecraft", "Набор Minecraft", 64.99, 13, 0, 0),
    ("Кукла Winx", "Фея Winx", 22.99, 28, 1, 1),
    ("Playmobil Полиция", "Полицейский участок", 54.99, 10, 6, 3),
    ("Конструктор деревянный", "Деревянные кубики", 27.99, 25, 5, 4),
    ("Плюшевый единорог", "Радужный единорог", 32.99, 20, 4, 4),
    ("LEGO Creator", "Универсальный набор", 74.99, 11, 0, 0),
    ("Barbie Профессии", "Кукла врач", 26.99, 24, 1, 1),
    ("Машинка пожарная", "Большая пожарная машина", 39.99, 17, 2, 2),
    ("Настольная игра Джанга", "Башня из брусочков", 18.99, 33, 3, 2),
    ("Playmobil Пираты", "Пиратский корабль", 79.99, 9, 6, 3),
]

products = []
for data in products_data:
    product = Product.objects.create(
        name=data[0],
        description=data[1],
        price=Decimal(str(data[2])),
        stock_quantity=data[3],
        category=categories[data[4]],
        manufacturer=manufacturers[data[5]]
    )
    products.append(product)

print(f"Создано товаров: {len(products)}")

# === 4. Пользователи и корзины (5 шт.) ===
for i in range(5):
    username = f"user{i+1}"
    user = User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password="password123"
    )
    
    cart = Cart.objects.create(user=user)
    
    # Добавляем 2-3 товара в корзину
    CartItem.objects.create(cart=cart, product=products[i*2], quantity=1)
    CartItem.objects.create(cart=cart, product=products[i*2 + 1], quantity=2)
    if i < 3:
        CartItem.objects.create(cart=cart, product=products[i*2 + 5], quantity=1)

print(f"Создано пользователей: 5")

print("\nБаза данных успешно заполнена!")
print(f" Производителей: {Manufacturer.objects.count()}")
print(f" Категорий: {Category.objects.count()}")
print(f" Товаров: {Product.objects.count()}")
print(f" Пользователей: {User.objects.filter(username__startswith='user').count()}")