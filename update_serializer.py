with open('store/serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = "fields = ['id', 'username', 'email', 'full_name', 'phone', 'address', 'role', 'avatar']"
new = "fields = ['id', 'username', 'email', 'full_name', 'phone', 'address', 'delivery_city', 'postal_code', 'favorite_category', 'newsletter', 'role', 'avatar']"

content = content.replace(old, new)

with open('store/serializers.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Сериализатор обновлён!')
