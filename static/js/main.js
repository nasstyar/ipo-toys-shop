// Основные функции магазина игрушек

// Функция для получения CSRF-токена
function getCSRFToken() {
    const cookie = document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

// Функция для показа уведомлений (Bootstrap Toast)
function showAlert(message, type = 'success') {
    // Создаём toast-уведомление
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.cssText = 'z-index: 9999;';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : type === 'danger' ? 'bg-danger' : 'bg-info';
    const icon = type === 'success' ? 'check-circle' : type === 'danger' ? 'x-circle' : 'info-circle';
    
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${icon}"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    document.getElementById('toast-container').insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
    // Удаляем после закрытия
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.remove();
    });
}

// Функция загрузки товаров из API
async function loadProducts() {
    const container = document.getElementById('product-list');
    if (!container) return;
    
    // Показываем спиннер
    container.innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-danger" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="mt-3 text-muted">Загрузка товаров...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/products/');
        if (!response.ok) throw new Error('Ошибка загрузки товаров');
        
        const data = await response.json();
        const products = data.results || data;
        
        if (products.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i> Товары не найдены
                    </div>
                </div>
            `;
            return;
        }
        
        renderProducts(products);
    } catch (error) {
        console.error('Ошибка:', error);
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle"></i> Не удалось загрузить товары. Попробуйте позже.
                </div>
            </div>
        `;
    }
}

// Функция рендеринга товаров
function renderProducts(products) {
    const container = document.getElementById('product-list');
    if (!container) return;
    
    container.innerHTML = '';
    
    products.forEach(product => {
        const photoHtml = product.photo 
            ? `<img src="${product.photo}" class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover;">`
            : `<div class="card-img-top d-flex align-items-center justify-content-center bg-light" style="height: 200px;">
                 <i class="bi bi-image" style="font-size: 3rem; color: #ff6b9d;"></i>
               </div>`;
        
        const card = `
            <div class="col-sm-6 col-md-4 col-lg-3 mb-4">
                <div class="card h-100" style="border: none; box-shadow: 0 2px 8px rgba(255, 107, 157, 0.15); border-radius: 15px;">
                    ${photoHtml}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title" style="color: #c9184a; font-weight: 600;">${product.name}</h5>
                        <p class="card-text text-muted small flex-grow-1">${product.description || ''}</p>
                        <p style="color: #c9184a; font-weight: bold; font-size: 1.4rem; margin-top: auto;">${product.price} руб.</p>
                        <div class="mt-3">
                            <a href="/product/${product.id}/" class="btn btn-outline-primary w-100 mb-2" style="border-radius: 25px; border-color: #ff6b9d; color: #ff6b9d;">
                                <i class="bi bi-eye"></i> Подробнее
                            </a>
                            <button onclick="addToCart(${product.id})" class="btn btn-primary w-100" style="border-radius: 25px; background-color: #ff6b9d; border-color: #ff6b9d;">
                                <i class="bi bi-cart-plus"></i> В корзину
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}

// Функция добавления в корзину через API
async function addToCart(productId) {
    const button = event.target.closest('button');
    const originalHtml = button.innerHTML;
    
    // Показываем спиннер на кнопке
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Добавление...';
    
    try {
        const csrfToken = getCSRFToken();
        const response = await fetch('/api/cart-items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ 
                product_id: productId, 
                quantity: 1 
            }),
        });
        
        if (response.ok) {
            const data = await response.json();
            showAlert('Товар добавлен в корзину!', 'success');
            
            // Обновляем счётчик корзины если есть
            updateCartCount();
        } else if (response.status === 401 || response.status === 403) {
            showAlert('Пожалуйста, войдите в систему', 'danger');
            setTimeout(() => {
                window.location.href = '/accounts/login/';
            }, 2000);
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Ошибка добавления товара', 'danger');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showAlert('Ошибка соединения с сервером', 'danger');
    } finally {
        // Возвращаем кнопку в исходное состояние
        button.disabled = false;
        button.innerHTML = originalHtml;
    }
}

// Обновление счётчика корзины
async function updateCartCount() {
    try {
        const response = await fetch('/api/carts/my-cart/');
        if (response.ok) {
            const data = await response.json();
            const count = data.items ? data.items.reduce((sum, item) => sum + item.quantity, 0) : 0;
            
            const badge = document.getElementById('cart-count');
            if (badge && count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline';
            }
        }
    } catch (error) {
        console.error('Не удалось обновить счётчик корзины:', error);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Магазин игрушек загружен!');
    
    // Если есть элемент product-list - загружаем товары
    if (document.getElementById('product-list')) {
        loadProducts();
    }
    
    // Обновляем счётчик корзины
    updateCartCount();
});

