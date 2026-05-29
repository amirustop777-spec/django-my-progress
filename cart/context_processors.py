from .cart import Cart

# Context processor — это функция, которая автоматически добавляет данные
# во ВСЕ шаблоны (если используется стандартная логика рендера Django).
#
# Здесь мы добавляем объект корзины в шаблоны под ключом `cart`.
# Тогда в любом шаблоне можно писать: {{ cart }} / {{ cart.get_total_price }}.

def cart(request):
    # Cart берёт данные из request.session, поэтому ей нужен текущий запрос.
    return {'cart': Cart(request)}

