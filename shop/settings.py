
from pathlib import Path
import os

# BASE_DIR — путь до корня проекта.
BASE_DIR = Path(__file__).resolve().parent.parent


# В DEVELOPMENT (пока учишься) включаем DEBUG.
# В продакшене нужно выключать.
DEBUG = True

# SECRET_KEY — ключ для криптографии Django.
# В продакшене его нельзя коммитить/показывать.
SECRET_KEY = 'django-insecure-+a69^v2)jso17u+)!fnu27aqg463--5b3dodn#q$0=w$olhan+'

# ALLOWED_HOSTS ограничивает домены, с которых принимаются запросы.
# Для разработки можно оставлять пустым/добавлять localhost.
ALLOWED_HOSTS = []


# Подключаем приложения.
# Важно: сюда добавлены 'main' и 'cart'.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
    'cart',
]


# Middleware — цепочка «прослоек» между запросом и ответом.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Где лежат root-URL конфиги.
ROOT_URLCONF = 'shop.urls'


# Настройки шаблонов.
# APP_DIRS=True позволяет Django искать шаблоны внутри папок apps.
# В context_processors добавлен наш processor для корзины.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Этот processor добавляет в шаблоны переменную `cart`.
                'cart.context_processors.cart',
            ],
        },
    },
]


# WSGI application.
WSGI_APPLICATION = 'shop.wsgi.application'


# Настройки базы данных.
# Сейчас используется SQLite.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Парольные валидаторы (какие правила применяются к паролям).
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Локализация.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static/Media:
# STATIC_URL — где Django отдаёт статику (CSS/JS).
STATIC_URL = '/static/'

# Здесь в исходном проекте есть потенциальная ошибка:
# STATIC_ROOT используется дважды, и второй раз перезаписывается для media.
# Мы не меняем логику, но важно понимать смысл.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'media')


# Ключ в session, под которым хранится корзина.
# В Cart берётся: request.session.get(CART_SESSION_ID)
CART_SESSION_ID = 'cart'

