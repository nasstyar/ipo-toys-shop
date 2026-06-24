with open('store/templates/store/profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем отображение роли
old_role = '<p class="small text-muted">Роль: <span id="display-role">Покупатель</span></p>'
new_role = '''<div class="mb-3">
    <span class="badge" id="role-badge" style="font-size: 0.9rem; padding: 8px 16px;">
        <i class="bi bi-shield-check"></i> <span id="display-role">Покупатель</span>
    </span>
</div>'''

content = content.replace(old_role, new_role)

# Добавляем новые поля после address
old_address = '<textarea name="address" id="address" class="form-control" rows="2" placeholder="Город, улица, дом"></textarea>'
new_fields = old_address + '''
                <div class="row mt-3">
                    <div class="col-md-6 mb-3">
                        <label class="form-label"><i class="bi bi-geo-alt"></i> Город доставки</label>
                        <input type="text" name="delivery_city" id="delivery_city" class="form-control" placeholder="Москва">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label"><i class="bi bi-mailbox"></i> Почтовый индекс</label>
                        <input type="text" name="postal_code" id="postal_code" class="form-control" placeholder="101000">
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label"><i class="bi bi-star"></i> Любимая категория</label>
                    <select name="favorite_category" id="favorite_category" class="form-select">
                        <option value="">-- Не выбрана --</option>
                    </select>
                </div>
                <div class="form-check mb-3">
                    <input type="checkbox" name="newsletter" id="newsletter" class="form-check-input">
                    <label class="form-check-label" for="newsletter">
                        <i class="bi bi-envelope"></i> Подписаться на новости и акции
                    </label>
                </div>'''

content = content.replace(old_address, new_fields)

with open('store/templates/store/profile.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Личный кабинет обновлён!')
