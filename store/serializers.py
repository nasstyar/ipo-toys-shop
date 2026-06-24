from rest_framework import serializers
from .models import Category, Manufacturer, Product, Cart, CartItem


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории товара"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ManufacturerSerializer(serializers.ModelSerializer):
    """Сериализатор для производителя"""
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'description']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товара"""
    category = CategorySerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(),
        source='manufacturer',
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'photo', 'price',
            'stock_quantity', 'category', 'manufacturer',
            'category_id', 'manufacturer_id'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор для элемента корзины"""
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
        required=False
    )
    item_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'item_cost']


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины"""
    items = CartItemSerializer(many=True, read_only=True)
    total_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_cost']
        read_only_fields = ['user', 'created_at']

from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'address', 'delivery_city', 'postal_code', 'favorite_category', 'newsletter', 'role', 'avatar']
        read_only_fields = ['username', 'role']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'phone']

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        phone = validated_data.pop('phone', '')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, full_name=full_name, phone=phone)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
