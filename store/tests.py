from django.test import TestCase, Client
from django.contrib.auth.models import User
from store.models import Profile, Product, Category, Manufacturer

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_profile_created(self):
        """Профиль создаётся автоматически при создании пользователя"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_fields(self):
        """Профиль имеет нужные поля"""
        profile = self.user.profile
        profile.full_name = 'Иванов Иван'
        profile.phone = '+79991234567'
        profile.address = 'Москва'
        profile.save()
        self.assertEqual(profile.full_name, 'Иванов Иван')
        self.assertEqual(profile.phone, '+79991234567')
        self.assertEqual(profile.address, 'Москва')
    
    def test_profile_str(self):
        """Строковое представление профиля"""
        self.assertIn('testuser', str(self.user.profile))


class AuthAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_me_authenticated(self):
        """GET /api/me/ доступен авторизованному пользователю"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 200)
    
    def test_me_unauthenticated(self):
        """GET /api/me/ недоступен неавторизованному"""
        response = self.client.get('/api/me/')
        self.assertIn(response.status_code, [401, 403])
    
    def test_login_success(self):
        """Вход с правильными данными"""
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_login_wrong_password(self):
        """Вход с неправильным паролем"""
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
    
    def test_logout(self):
        """Выход из системы"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/api/logout/')
        self.assertIn(response.status_code, [200, 302])


class ProductPermissionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass123')
        self.cat = Category.objects.create(name='Тест')
        self.man = Manufacturer.objects.create(name='Тест')
        self.product = Product.objects.create(
            name='Тестовый товар',
            description='Тестовое описание',
            price=100,
            category=self.cat,
            manufacturer=self.man,
            stock_quantity=10
        )
    
    def test_get_products_all(self):
        """GET /api/products/ доступен всем"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_product_detail(self):
        """GET конкретного товара доступен всем"""
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_product_requires_admin(self):
        """Создание товара требует прав администратора"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/api/products/', {})
        self.assertIn(response.status_code, [400, 401, 403])
    
    def test_products_list_not_empty(self):
        """Список товаров не пустой"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        results = data.get('results', data)
        self.assertGreater(len(results), 0)


class HomePageTest(TestCase):
    def test_home_page(self):
        """Главная страница загружается"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Магазин игрушек')
    
    def test_catalog_page(self):
        """Страница каталога загружается"""
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
    
    def test_profile_page_requires_login(self):
        """Страница профиля доступна авторизованным"""
        user = User.objects.create_user(username='testuser2', password='testpass123')
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
