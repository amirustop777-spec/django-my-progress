from django.contrib import admin

from .models import Category, Product

# Настройки админ-панели для моделей приложения main.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Какие поля показывать в списке категорий.
    list_display = ['name', 'slug']

    # Автозаполнение slug на основе name.
    # При вводе Django заполнит slug автоматически (если это поле в форме).
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Поля, которые показываются в списке товаров.
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']

    # Боковые фильтры в админке.
    list_filter = ['available', 'created', 'updated', 'category']

    # Какие поля можно редактировать прямо в таблице.
    list_editable = ['price', 'available']

    # Автозаполнение slug на основе name.
    prepopulated_fields = {'slug': ('name',)}

