from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from main.models import Product

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """Добавить товар в корзину или обновить его количество."""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        # override=True => перезаписываем quantity
        # override=False => увеличиваем quantity
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
        )

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Удалить товар из корзины."""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    """Страница корзины.

    В шаблон передаём объект Cart.

    Для каждого item создаём отдельную форму
    `update_quantity_form`, чтобы пользователь мог обновить количество.
    """

    cart = Cart(request)

    for item in cart:
        # override=True означает: при сабмите мы установим quantity заново.
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
            }
        )

    return render(request, 'cart/cart_detail.html', {'cart': cart})

