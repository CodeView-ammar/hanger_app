from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns  # لدعم التعدد اللغوي

urlpatterns = [
    # لتغيير اللغة من الواجهة (مثلاً من نموذج اختيار اللغة)
    path('i18n/', include('django.conf.urls.i18n')),
    
    # روابط التطبيقات العامة أو API
    # path('services/', include('services.urls')),  # مثال لتطبيق الخدمات
    # path('orders/', include('orders.urls')),      # يمكنك تكرار السطر لتطبيقات أخرى
    # path('accounts/', include('accounts.urls')),
    # ...
]

# لوحة التحكم والإدارات الداخلية بلغة الموقع (العربية هنا)
# urlpatterns += i18n_patterns(
#     path('admin/', admin.site.urls),
#     prefix_default_language=False  # لإخفاء /ar/ من الرابط
# )

# الملفات الثابتة والإعلامية أثناء التطوير
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
