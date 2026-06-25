from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product, Category, Manufacturer, Cart, CartItem


def home(request):
    from .models import Product, Category
    popular_products = Product.objects.all()[:6]
    categories = Category.objects.all()
    context = {
        'popular_products': popular_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def about_author(request):
    return HttpResponse("""
<h1>Об авторе</h1>
<p>Лабораторную работу выполнила: Козлова Анастасия</p>
<p>Группа: 87ТП</p>
<p>Учебное заведение: МГКЦТ</p>
""")


def about_store(request):
    return HttpResponse("""
<h1>О магазине</h1>
<p><strong>Тема лабораторной работы:</strong> Магазин игрушек для детей</p>
<p>Данный проект демонстрирует базовую настройку Django-приложения для интернет-магазина.</p>
""")


def product_list(request):
    products = Product.objects.all().order_by('id')
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    # Фильтры
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)
    
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Пагинация - 9 товаров на странице
    from django.core.paginator import Paginator
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'categories': categories,
        'manufacturers': manufacturers,
    }
    return render(request, 'store/catalog.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        if cart_item.quantity > product.stock_quantity:
            cart_item.quantity = product.stock_quantity
            messages.warning(request, f'Достигнуто максимальное количество ({product.stock_quantity} шт.)')
        cart_item.save()
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    return redirect('home')


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    if cart_item.cart.user != request.user:
        messages.error(request, 'Вы не можете изменять чужую корзину!')
        return redirect('cart')
    new_quantity = int(request.POST.get('quantity', 1))
    if new_quantity > cart_item.product.stock_quantity:
        messages.warning(request, f'Нельзя добавить больше {cart_item.product.stock_quantity} шт.')
        new_quantity = cart_item.product.stock_quantity
    if new_quantity <= 0:
        cart_item.delete()
        messages.success(request, f'Товар "{cart_item.product.name}" удалён из корзины')
    else:
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'Количество товара "{cart_item.product.name}" обновлено')
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    if cart_item.cart.user != request.user:
        messages.error(request, 'Вы не можете удалять товары из чужой корзины!')
        return redirect('cart')
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Товар "{product_name}" удалён из корзины')
    return redirect('cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_cost = cart.total_cost()
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'store/cart.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


import openpyxl
from django.core.mail import EmailMessage
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.warning(request, 'Ваша корзина пуста!')
        return redirect('cart')

    total_cost = cart.total_cost()

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if not address or not phone or not email:
            messages.error(request, 'Пожалуйста, заполните все поля!')
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total_cost': total_cost,
            })

        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone,
            total_cost=total_cost
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Чек'

        ws.append(['Чек заказа #' + str(order.id)])
        ws.append(['Дата:', str(order.created_at)])
        ws.append(['Покупатель:', request.user.username])
        ws.append(['Адрес:', address])
        ws.append(['Телефон:', phone])
        ws.append([])
        ws.append(['Товар', 'Количество', 'Цена', 'Стоимость'])

        for item in cart_items:
            ws.append([
                item.product.name,
                item.quantity,
                float(item.product.price),
                float(item.item_cost())
            ])

        ws.append([])
        ws.append(['Итого:', '', '', float(total_cost)])

        file_path = f'order_{order.id}.xlsx'
        wb.save(file_path)

        email_msg = EmailMessage(
            subject=f'Чек заказа #{order.id}',
            body=f'Здравствуйте, {request.user.username}!\n\nВаш заказ #{order.id} успешно оформлен.\nАдрес доставки: {address}\nТелефон: {phone}\nОбщая сумма: {total_cost} руб.\n\nСпасибо за покупку!',
            from_email='shop@example.com',
            to=[email]
        )

        with open(file_path, 'rb') as f:
            email_msg.attach(f'chek_zakaz_{order.id}.xlsx', f.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        email_msg.send()

        import os
        os.remove(file_path)

        cart_items.delete()

        messages.success(request, f'Заказ #{order.id} успешно оформлен! Чек отправлен на {email}')
        return redirect('home')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
    })

# ========== API-представления (Django REST Framework) ==========

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    OrderSerializer,
    CategorySerializer, ManufacturerSerializer, ProductSerializer,
    CartSerializer, CartItemSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """API для работы с категориями товаров"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ManufacturerViewSet(viewsets.ModelViewSet):
    """API для работы с производителями"""
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """API для работы с товарами с фильтрацией"""
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        manufacturer = self.request.query_params.get('manufacturer')
        search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category_id=category)
        if manufacturer:
            queryset = queryset.filter(manufacturer_id=manufacturer)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class CartViewSet(viewsets.ModelViewSet):
    """API для работы с корзиной пользователя"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    """API для работы с элементами корзины"""
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import OrderSerializer, ProfileSerializer, UserRegisterSerializer, UserLoginSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({
                'id': user.id,
                'username': user.username,
                'message': 'Регистрация успешна'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return Response({
                    'id': user.id,
                    'username': user.username,
                    'message': 'Вход выполнен'
                })
            return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен'})

def profile_view(request):
    from .models import Category
    categories = Category.objects.all()
    return render(request, 'store/profile.html', {'categories': categories})


def settings_view(request):
    return render(request, 'store/settings.html')


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
