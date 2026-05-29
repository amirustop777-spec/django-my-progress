from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    """Главная страница/страница списка товаров.

    Если category_slug передан — показываем товары только выбранной категории.
    В любом случае скрываем товары, у которых available=False.
    """

    # Список категорий для меню/фильтра.
    categories = Category.objects.all()

    # Базовый набор товаров: только доступные.
    products = Product.objects.filter(available=True)

    # Если категория не выбрана — category=None.
    category = None

    # Если в URL есть категория — подгружаем её из БД.
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

        # И добавляем фильтр по выбранной категории.
        products = products.filter(category=category)

    # Рендерим шаблон, передавая:
    # - category (выбрана/не выбрана)
    # - categories (все категории)
    # - products (подходящие товары)
    return render(
        request,
        'main/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
        },
    )


def product_detail(request, id, slug):
    """Карточка товара.

    Ищем товар по (id, slug) и проверяем доступность (available=True).
    Также показываем «похожие товары» из той же категории.
    """

    # get_object_or_404 вернёт 404, если товара нет.
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True,
    )

    # Похожие товары:
    # - те же категория
    # - доступные
    # - не тот же самый товар
    # - максимум 4 штуки
    related_products = (
        Product.objects.filter(
            category=product.category,
            available=True,
        )
        .exclude(id=product.id)[:4]
    )

    # Форма для добавления товара в корзину.
    cart_product_form = CartAddProductForm()

    return render(
        request,
        'main/product/detail.html',
        {
            'product': product,
            'related_products': related_products,
            'cart_product_form': cart_product_form,
        },
    )
