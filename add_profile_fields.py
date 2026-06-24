with open('store/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим поле address и добавляем после него новые поля
old = "    address = models.TextField('Адрес', blank=True)"
new = """    address = models.TextField('Адрес', blank=True)
    delivery_city = models.CharField('Город доставки', max_length=100, blank=True)
    postal_code = models.CharField('Почтовый индекс', max_length=10, blank=True)
    favorite_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Любимая категория')
    newsletter = models.BooleanField('Подписка на новости', default=False)"""

content = content.replace(old, new)

with open('store/models.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Поля добавлены в модель!')
