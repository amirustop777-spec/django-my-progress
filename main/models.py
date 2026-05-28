from django.db import models
from django.urls import reverse

# модели для интернет-магазина

class Category(models.Model):
    # название категории с индексом для быстрого поиска
    name = models.CharField(max_length=100, db_index=True)
    # часть url-адреса, должна быть уникальной
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        # сортировка по алфавиту
        ordering = ('name', )
        # имя в админке (ед. число)
        verbose_name = 'Категория' 
        # имя в админке (мн. число)
        verbose_name_plural = 'Категории'

    def __str__(self):
        # возвращает имя при выводе объекта строкой
        return self.name


    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])
    
    
class Product(models.Model):
    # связь с категорией. при удалении категории удалятся и её товары
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # название товара с индексом
    name = models.CharField(max_length=100, db_index=True)
    # уникальный url-адрес товара
    slug = models.SlugField(max_length=100, unique=True)
    # путь для загрузки фото, поле необязательное
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    # описание товара, может быть пустым
    description = models.TextField(blank=True)
    # цена: максимум 10 цифр, из них 2 знака после запятой
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # статус наличия
    available = models.BooleanField(default=True)
    # дата создания, пишется один раз автоматически
    created = models.DateTimeField(auto_now_add=True)
    # дата обновления, меняется при каждом сохранении
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])