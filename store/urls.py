from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_author, name='about_author'),
    path('store-info/', views.about_store, name='about_store'),
]