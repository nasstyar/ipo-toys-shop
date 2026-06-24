with open('store/templates/store/settings.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends 'base.html' %}
{% load static %}

{% block title %}Настройки{% endblock %}

{% block content %}
<style>
.settings-card {
    border: none;
    box-shadow: 0 3px 15px rgba(255, 107, 157, 0.15);
    border-radius: 15px;
    padding: 2rem;
    background: white;
    margin-bottom: 2rem;
    max-width: 600px;
}
.settings-card h3 {
    color: #c9184a;
    margin-bottom: 1.5rem;
}
.form-control {
    border: 2px solid #ffc2d1;
    border-radius: 10px;
}
.form-control:focus {
    border-color: #ff6b9d;
    box-shadow: 0 0 0 0.2rem rgba(255, 107, 157, 0.25);
}
.btn-save {
    background: linear-gradient(135deg, #ff6b9d, #c9184a);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 30px;
    font-weight: 600;
}
.btn-save:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 107, 157, 0.4);
    color: white;
}
</style>

{% if user.is_authenticated %}
<h1 class="mb-4" style="color: #c9184a;">
    <i class="bi bi-gear"></i> Настройки
</h1>

<div class="row">
    <div class="col-md-6 mb-4">
        <div class="settings-card">
            <h3><i class="bi bi-key"></i> Смена пароля</h3>
            <form method="post" action="/accounts/password_change/">
                {% csrf_token %}
                <div class="mb-3">
                    <label class="form-label">Текущий пароль</label>
                    <input type="password" name="old_password" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Новый пароль</label>
                    <input type="password" name="new_password1" class="form-control" required minlength="8">
                </div>
                <div class="mb-3">
                    <label class="form-label">Подтверждение нового пароля</label>
                    <input type="password" name="new_password2" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-save">
                    <i class="bi bi-check-circle"></i> Сменить пароль
                </button>
            </form>
        </div>
    </div>

    <div class="col-md-6 mb-4">
        <div class="settings-card">
            <h3><i class="bi bi-envelope"></i> Смена Email</h3>
            <form id="email-form">
                <div class="mb-3">
                    <label class="form-label">Новый Email</label>
                    <input type="email" name="email" id="new-email" class="form-control" value="{{ user.email }}" required>
                </div>
                <button type="submit" class="btn btn-save">
                    <i class="bi bi-check-circle"></i> Сохранить Email
                </button>
            </form>
            <div id="email-message" class="mt-3"></div>
        </div>

        <div class="settings-card">
            <h3><i class="bi bi-bell"></i> Уведомления</h3>
            <form id="newsletter-form">
                <div class="form-check mb-3">
                    <input type="checkbox" name="newsletter" id="settings-newsletter" class="form-check-input">
                    <label class="form-check-label" for="settings-newsletter">
                        Получать новости и акции на почту
                    </label>
                </div>
                <button type="submit" class="btn btn-save">
                    <i class="bi bi-check-circle"></i> Сохранить
                </button>
            </form>
            <div id="newsletter-message" class="mt-3"></div>
        </div>
    </div>
</div>

{% else %}
<div class="text-center py-5">
    <i class="bi bi-shield-lock" style="font-size: 5rem; color: #ff6b9d;"></i>
    <h2 class="mt-3" style="color: #c9184a;">Доступ запрещён</h2>
    <p class="text-muted">Пожалуйста, войдите в систему</p>
    <a href="{% url 'login' %}" class="btn btn-primary btn-lg">
        <i class="bi bi-box-arrow-in-right"></i> Войти
    </a>
</div>
{% endif %}
{% endblock %}

{% block scripts %}
{% if user.is_authenticated %}
<script>
document.getElementById('email-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('new-email').value;
    const msgDiv = document.getElementById('email-message');
    
    try {
        const response = await fetch('/api/me/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ email: email }),
        });
        
        if (response.ok) {
            msgDiv.innerHTML = '<div class="alert alert-success"><i class="bi bi-check-circle"></i> Email обновлён!</div>';
        } else {
            msgDiv.innerHTML = '<div class="alert alert-danger"><i class="bi bi-x-circle"></i> Ошибка сохранения</div>';
        }
    } catch (error) {
        msgDiv.innerHTML = '<div class="alert alert-danger"><i class="bi bi-x-circle"></i> Ошибка соединения</div>';
    }
    setTimeout(() => { msgDiv.innerHTML = ''; }, 3000);
});

document.getElementById('newsletter-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const newsletter = document.getElementById('settings-newsletter').checked;
    const msgDiv = document.getElementById('newsletter-message');
    
    try {
        const response = await fetch('/api/me/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ newsletter: newsletter }),
        });
        
        if (response.ok) {
            msgDiv.innerHTML = '<div class="alert alert-success"><i class="bi bi-check-circle"></i> Настройки сохранены!</div>';
        } else {
            msgDiv.innerHTML = '<div class="alert alert-danger"><i class="bi bi-x-circle"></i> Ошибка</div>';
        }
    } catch (error) {
        msgDiv.innerHTML = '<div class="alert alert-danger"><i class="bi bi-x-circle"></i> Ошибка соединения</div>';
    }
    setTimeout(() => { msgDiv.innerHTML = ''; }, 3000);
});

function getCookie(name) {
    const value = '; ' + document.cookie;
    const parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}
</script>
{% endif %}
{% endblock %}''')
print('✅ Страница настроек создана!')
