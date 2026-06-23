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
