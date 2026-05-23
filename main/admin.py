from django.contrib import admin
from .models import Category, Product

# регистрация моделей в админ-панели

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # колонки, которые будут видны в списке категорий
    list_display = ['name', 'slug']
    # автоматическое заполнение слага на основе имени при вводе
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # колонки, которые будут видны в списке товаров
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    # правая панель с фильтрами для быстрой сортировки
    list_filter = ['available', 'created', 'updated', 'category']
    # поля, которые можно редактировать прямо в списке, не заходя в товар
    list_editable = ['price', 'available']
    # автоматическое заполнение слага для товара
    prepopulated_fields = {'slug': ('name', )}