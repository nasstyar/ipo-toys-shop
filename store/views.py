# from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Главная страница с ссылками"""
    return HttpResponse("""
    <h1>Добро пожаловать в магазин!</h1>
    <ul>
        <li><a href="/about/">Об авторе</a></li>
        <li><a href="/store-info/">О магазине</a></li>
    </ul>
    """)

def about_author(request):
    """Страница об авторе"""
    return HttpResponse("""
    <h1>Об авторе</h1>
    <p>Лабораторную работу выполнила: Козлова Анастасия</p>
    <p>Группа: 87ТП</p>
    <p>Учебное заведение: МГКЦТ</p>
    """)

def about_store(request):
    """Страница о магазине игрушек для детей"""
    return HttpResponse("""
    <h1>О магазине</h1>
    <p><strong>Тема лабораторной работы:</strong> Магазин игрушек для детей</p>
    <p>Данный проект демонстрирует базовую настройку Django-приложения 
    для интернет-магазина.</p>
    <p>Функционал: маршрутизация, представления, статические страницы.</p>
    """)
