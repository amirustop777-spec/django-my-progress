from django.urls import path

from . import views

app_name = 'main'

# URL-пути для app "main".
# Имена (name=...) нужны для шаблонов, чтобы писать {% url 'main:product_detail' %}
urlpatterns = [
    # /  → список товаров
    path('', views.product_list, name='product_list'),

    # /<category_slug>/ → список товаров по категории
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category',
    ),

    # /<id>/<slug> → карточка товара
    path(
        '<int:id>/<slug:slug>',
        views.product_detail,
        name='product_detail',
    ),
]

