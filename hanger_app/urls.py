from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# urlpatterns = (
#     [
#         path("i18n/", include("django.conf.urls.i18n")),
#     ]
#     + i18n_patterns(
#         path("admin/", admin.site.urls),
#     )
# )
urlpatterns = ([
    # path('admin/', admin.site.urls),
        path('api/', include('users.urls')),
    path('api/', include('laundries.urls')),  # Include your app's URLs
    path('api/', include('settings.urls')),  # Include your app's URLs
    path('api/notifications/', include('notification.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/', include('services.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('agent.urls')),
    path('api/', include('support.urls')),
    path('', include('website.urls')),
    
    # path('api/', include('invoices.urls')),
    # path('api/', include('transactions.urls')),
    # path('api/', include('reviews.urls')),
    # path('api/', include('addresses.urls')),
]+ i18n_patterns(
        path("admin/", admin.site.urls),
    )
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = "Hanger Admin"
admin.site.site_title = "Hanger Admin Portal"
admin.site.index_title = "Welcome to Hanger Researcher Portal"
