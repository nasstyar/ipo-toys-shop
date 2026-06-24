# Добавляем view
with open('store/views.py', 'a', encoding='utf-8') as f:
    f.write('''

def settings_view(request):
    return render(request, 'store/settings.html')
''')
print('✅ View добавлен!')

# Добавляем URL
with open('store/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'settings/' not in content:
    content = content.replace(
        "path('profile/', views.profile_view, name='profile'),",
        "path('profile/', views.profile_view, name='profile'),\n    path('settings/', views.settings_view, name='settings'),"
    )
    with open('store/urls.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ URL добавлен!')
else:
    print('✅ URL уже есть!')
