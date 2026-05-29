from django.conf import settings
from main.models import Product


class Cart:
    """Корзина, которая хранится в сессии (session) пользователя.

    Почему session:
    - не требуется регистрация пользователя
    - корзина живёт между запросами, пока сессия активна

    Как устроено хранение:
    self.cart — это словарь вида:
        {
          'product_id': {'quantity': int, 'price': 'строка' }
        }

    Ключи делаем строками, потому что JSON/сериализация session часто
    предпочитает строковые ключи.
    """

    def __init__(self, request):
        # request.session — это хранилище данных на стороне сервера,
        # связанное с текущим пользователем через cookie.
        self.session = request.session

        # Достаём корзину из сессии.
        cart = self.session.get(settings.CART_SESSION_ID)

        # Если корзины ещё нет — создаём пустой словарь в session.
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        # Ссылка на словарь корзины.
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Добавляет товар в корзину.

        override_quantity=False:
          увеличиваем quantity
        override_quantity=True:
          перезаписываем quantity значением quantity
        """

        # ID товара в виде строки (см. докстринг класса).
        product_id = str(product.id)

        # Если товара ещё нет в корзине — создаём запись.
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                # price сохраняем как строку, чтобы не получить проблемы
                # с сериализацией Decimal.
                'price': str(product.price),
            }

        # Обновляем количество.
        if override_quantity:
            # Например, пользователь ввёл новое количество в форме.
            self.cart[product_id]['quantity'] = quantity
        else:
            # Например, пользователь нажал «Добавить в корзину».
            self.cart[product_id]['quantity'] += quantity

        # Помечаем сессию как изменённую — чтобы Django сохранил её.
        self.save()

    def save(self):
        # Без этого некоторые backends могут не записать session в БД.
        self.session.modified = True

    def remove(self, product):
        """Удаляет товар из корзины."""

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Позволяет делать: for item in cart.

        На лету:
        - подтягиваем Product из БД
        - рассчитываем total_price
        - добавляем ключ 'product' в каждый item
        """

        # IDs товаров, которые лежат в корзине.
        product_ids = self.cart.keys()

        # Забираем товары из БД за один запрос.
        products = Product.objects.filter(id__in=product_ids)

        # Копия корзины, чтобы не мутировать оригинал при расчётах.
        cart = self.cart.copy()

        # Добавляем в каждую запись экземпляр Product.
        for product in products:
            cart[str(product.id)]['product'] = product

        # Превращаем данные в удобный формат для шаблона.
        for item in cart.values():
            # В session price лежит строкой → переводим в float.
            item['price'] = float(item['price'])
            # Общая стоимость позиции.
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Количество всех товаров в корзине (сумма quantities)."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Итоговая стоимость всей корзины."""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Полное очищение корзины."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

                   

    
