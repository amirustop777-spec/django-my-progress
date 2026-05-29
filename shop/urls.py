from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Основная точка маршрутизации (root urls).
# Django смотрит сюда, чтобы понять: какой view вызывать для каждого URL.
urlpatterns = [
    # /admin/ → панель администратора
    path('admin/', admin.site.urls),

    # /cart/... → маршруты app cart
    path('cart/', include('cart.urls', namespace='cart')),

    # /... → маршруты app main (магазин)
    path('', include('main.urls', namespace='main')),
]

# В режиме DEBUG Django не умеет по умолчанию отдавать MEDIA-файлы,
# поэтому добавляем статическую подачу медиа-контента.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

