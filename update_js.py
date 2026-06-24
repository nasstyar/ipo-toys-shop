with open('store/templates/store/profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_js = '''// Загрузка профиля
async function loadProfile() {
    try {
        const response = await fetch('/api/me/');
        if (response.status === 401) {
            window.location.href = '/accounts/login/';
            return;
        }
        const data = await response.json();
        
        document.getElementById('display-name').textContent = data.full_name || data.username;
        document.getElementById('display-email').textContent = data.email;
        document.getElementById('display-role').textContent = data.role === 'ADMIN' ? 'Администратор' : 'Покупатель';
        
        document.getElementById('full_name').value = data.full_name || '';
        document.getElementById('email').value = data.email || '';
        document.getElementById('phone').value = data.phone || '';
        document.getElementById('address').value = data.address || '';
    } catch (error) {
        console.error('Ошибка загрузки профиля:', error);
    }
}'''

new_js = '''// Загрузка категорий
async function loadCategories() {
    try {
        const response = await fetch('/api/categories/');
        const data = await response.json();
        const categories = data.results || data;
        const select = document.getElementById('favorite_category');
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Ошибка загрузки категорий:', error);
    }
}

// Загрузка профиля
async function loadProfile() {
    try {
        const response = await fetch('/api/me/');
        if (response.status === 401) {
            window.location.href = '/accounts/login/';
            return;
        }
        const data = await response.json();
        
        document.getElementById('display-name').textContent = data.full_name || data.username;
        document.getElementById('display-email').textContent = data.email;
        
        const roleSpan = document.getElementById('display-role');
        const roleBadge = document.getElementById('role-badge');
        if (data.role === 'ADMIN') {
            roleSpan.textContent = 'Администратор';
            roleBadge.style.background = 'linear-gradient(135deg, #c9184a, #ff6b9d)';
            roleBadge.style.color = 'white';
        } else if (data.role === 'MANAGER') {
            roleSpan.textContent = 'Менеджер';
            roleBadge.style.background = 'linear-gradient(135deg, #ffb703, #fb8500)';
            roleBadge.style.color = 'white';
        } else {
            roleSpan.textContent = 'Покупатель';
            roleBadge.style.background = 'linear-gradient(135deg, #f8bbd0, #f48fb1)';
            roleBadge.style.color = '#c9184a';
        }
        
        document.getElementById('full_name').value = data.full_name || '';
        document.getElementById('email').value = data.email || '';
        document.getElementById('phone').value = data.phone || '';
        document.getElementById('address').value = data.address || '';
        document.getElementById('delivery_city').value = data.delivery_city || '';
        document.getElementById('postal_code').value = data.postal_code || '';
        if (data.favorite_category) {
            document.getElementById('favorite_category').value = data.favorite_category;
        }
        document.getElementById('newsletter').checked = data.newsletter || false;
    } catch (error) {
        console.error('Ошибка загрузки профиля:', error);
    }
}'''

content = content.replace(old_js, new_js)
content = content.replace('loadProfile();\n    loadOrders();', 'loadCategories();\n    loadProfile();\n    loadOrders();')

with open('store/templates/store/profile.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ JavaScript обновлён!')
