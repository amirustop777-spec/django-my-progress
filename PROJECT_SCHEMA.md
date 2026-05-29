# Схема проекта (Django интернет-магазин) — для обучения

Ниже — «картинка» того, как связаны части проекта.

---

## 1) Django-проект

- **`shop/`** — ядро Django-проекта
  - `settings.py` — настройки (INSTALLED_APPS, middleware, шаблоны, статика, медиа, сессии и т.д.)
  - `urls.py` — подключение url’ов приложения
  - `wsgi.py`, `asgi.py` — точки входа для развёртывания

---

## 2) Приложение `main`

- **`main/`** — каталог товаров + страницы списка/карточки
  - `models.py` — модели магазина:
    - `Category` — категории (с `slug` для URL)
    - `Product` — товары (с `category`, `slug`, `price`, `available` и т.д.)
  - `views.py` — обработчики:
    - `product_list` — список товаров (возможна фильтрация по категории)
    - `product_detail` — страница товара + связанные товары
  - `urls.py` — маршруты:
    - `/` → `product_list`
    - `/<category_slug>/` → `product_list_by_category`
    - `/<id>/<slug>/` → `product_detail`
  - `admin.py` — регистрация моделей в админке
  - `templates/main/` — HTML-шаблоны:
    - `base.html`
    - `product/list.html`
    - `product/detail.html`

---

## 3) Приложение `cart`

- **`cart/`** — корзина на сессии
  - `cart.py` — класс `Cart`, который:
    - хранит корзину в `request.session`
    - умеет `add`, `remove`, `__iter__`, `get_total_price`, `clear`
  - `forms.py` — форма для обновления количества в корзине
  - `views.py` — обработчики POST-запросов:
    - `cart_add` — добавить в корзину / изменить количество
    - `cart_remove` — удалить товар
    - `cart_detail` — отрисовать страницу корзины
  - `urls.py` — маршруты для корзины:
    - `/` → `cart_detail`
    - `/add/<product_id>/` → `cart_add`
    - `/remove/<product_id>/` → `cart_remove`
  - `context_processors.py` — пробрасывает `cart` в шаблоны автоматически
  - `templates/cart/` — HTML-шаблон страницы корзины:
    - `cart_detail.html`
  - `admin.py` — (если используется) регистрация моделей корзины (обычно корзина — это не модель БД)

---

## 4) Связи между частями

### Поток запроса к страницам товара

1. Браузер запрашивает URL товара/каталога
2. `shop/urls.py` → подключает `main/urls.py`
3. Django вызывает нужный view из `main/views.py`
4. view читает данные через ORM (из `main/models.py`)
5. view рендерит шаблон из `main/templates/main/...`

### Корзина

1. Страница товара (`main/product/detail.html`) содержит форму добавления в корзину
2. POST уходит в `cart/views.py` (`cart_add`)
3. `cart_add` валидирует форму и вызывает `Cart.add(...)`
4. `Cart` записывает данные в `request.session`
5. Затем происходит редирект на `cart_detail`
6. `cart/context_processors.py` добавляет `cart` в контекст шаблонов
7. `cart/templates/cart/cart_detail.html` показывает таблицу и итог

---

## 5) Мини-список «что за что отвечает»

- **Модели** (`main/models.py`) — структура данных БД
- **Views** (`main/views.py`, `cart/views.py`) — логика обработки запросов
- **URLs** (`main/urls.py`, `cart/urls.py`, `shop/urls.py`) — маршрутизация
- **Шаблоны** (`templates/...`) — представление HTML
- **Cart** (`cart/cart.py`) — бизнес-логика корзины, хранение в сессии
- **Context processor** — автоматическое добавление `cart` в шаблоны

---

## 6) Быстрые ориентиры по структуре директорий

- `shop/` : проект
- `main/` : товары и страницы каталога
- `cart/` : корзина поверх сессии
- `templates/` : HTML

---

### Примечание
Этот проект использует *сессии* для корзины (а не отдельные таблицы в БД для корзины). Это упрощает обучение и позволяет демонстрировать логику без сложной схемы заказа.

