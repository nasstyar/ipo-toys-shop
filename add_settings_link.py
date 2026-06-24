with open('store/templates/store/profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_link = '<a href="/catalog/" class="btn btn-outline-primary">'
new_link = '<a href="/settings/" class="btn btn-outline-primary"><i class="bi bi-gear"></i> Настройки</a>\n                <a href="/catalog/" class="btn btn-outline-primary">'

content = content.replace(old_link, new_link)

with open('store/templates/store/profile.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Ссылка добавлена!')
