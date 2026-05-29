from django.db import models
from django.urls import reverse

# =========================
# МОДЕЛИ ИНТЕРНЕТ-МАГАЗИНА
# =========================
# Django-модель — это класс, который описывает таблицу в базе данных.
# На основе моделей автоматически создаются поля, миграции и интерфейсы.


class Category(models.Model):
    """Категория товаров.

    Описание:
    - name — отображаемое имя категории.
    - slug — «красивый» идентификатор для URL (например, /category/telefon/).

    Практика:
    - slug обычно уникален, чтобы URL не конфликтовали.
    """

    # Название категории.
    # db_index=True создаёт индекс в БД для ускорения фильтраций/поиска по имени.
    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Отображаемое имя категории",
    )

    # Часть URL. Django проверяет корректность slug (только допустимые символы).
    # unique=True гарантирует уникальность значения в таблице.
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Уникальный идентификатор для URL",
    )

    class Meta:
        # ordering — стандартная сортировка, если явно не задали сортировку в запросе.
        ordering = ('name',)

        # Названия в админке Django.
        verbose_name = 'Категория'          # как назвать один объект
        verbose_name_plural = 'Категории'  # как назвать несколько объектов

    def __str__(self):
        """Строковое представление объекта.

        Django использует это значение в админке и в списках.
        """

        return self.name

    def get_absolute_url(self):
        """Возвращает ссылку на страницу со списком товаров выбранной категории.

        reverse(...) ищет URL по имени роута в urls.py.
        Args — параметры, которые роут ожидает (тут — slug).
        """

        return reverse(
            "main:product_list_by_category",
            args=[self.slug],
        )


class Product(models.Model):
    """Товар.

    Идеи дизайна:
    - Товар относится к одной категории.
    - Есть slug для URL карточки товара.
    - Поле available — «флаг активности», чтобы скрывать товары без удаления из БД.
    """

    # Связь с категорией.
    # related_name='products' — как обращаться к товарам из объекта Category.
    # Например: category.products.all().
    # on_delete=models.CASCADE — при удалении категории удалятся и её товары.
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        help_text="Категория, к которой относится товар",
    )

    # Название товара.
    # db_index=True — ускоряет запросы по названию.
    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Отображаемое имя товара",
    )

    # Уникальный slug товара для формирования URL карточки товара.
    # unique=True защищает от конфликтов ссылок.
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Уникальный идентификатор для URL товара",
    )

    # Изображение товара.
    # upload_to задаёт папку в MEDIA_ROOT (с шаблоном даты).
    # blank=True — поле может быть пустым в формах.
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        help_text="Изображение товара (опционально)",
    )

    # Описание товара.
    # blank=True — поле можно оставить пустым в формах.
    description = models.TextField(
        blank=True,
        help_text="Описание товара (опционально)",
    )

    # Цена товара.
    # DecimalField хранит число как Decimal (подходит для денег, чтобы избежать ошибок float).
    # max_digits — всего цифр, decimal_places — сколько знаков после запятой.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Цена товара",
    )

    # available — товар доступен/недоступен для показа.
    # default=True — по умолчанию товар считается доступным.
    available = models.BooleanField(
        default=True,
        help_text="Флаг доступности товара",
    )

    # created — дата создания.
    # auto_now_add=True заполняет поле один раз при первом сохранении.
    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата создания записи",
    )

    # updated — дата последнего обновления.
    # auto_now=True обновляет значение при каждом вызове save().
    updated = models.DateTimeField(
        auto_now=True,
        help_text="Дата последнего изменения записи",
    )

    class Meta:
        # Сортировка по умолчанию при запросах без явного order_by.
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        # Как товар выглядит в админке/списках.
        return self.name

    def get_absolute_url(self):
        """Возвращает ссылку на карточку товара.

        В urls.py должен существовать маршрут с именем main:product_detail,
        который принимает (id, slug) в args.
        """

        return reverse(
            "main:product_detail",
            args=[self.id, self.slug],
        )

