import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

with open('fixtures.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 
        'store.category',
        'store.manufacturer', 
        'store.product',
        'auth.user',
        indent=2, 
        stdout=f
    )

print('Готово!')

with open('fixtures.json', 'r', encoding='utf-8') as f:
    import json
    data = json.load(f)
    print(f'Всего объектов: {len(data)}')
    for item in data[:3]:
        name = item['fields'].get('name', 'N/A')
        print(f"  - {item['model']}: {name}")
