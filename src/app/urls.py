from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('shop-admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('shop.urls', namespace='shop')),
    path('summernote/', include('django_summernote.urls')),
]


handler400 = 'shop.error_handlers.bad_request'
handler403 = 'shop.error_handlers.permission_denied'
handler404 = 'shop.error_handlers.not_found'
handler500 = 'shop.error_handlers.server_error'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)