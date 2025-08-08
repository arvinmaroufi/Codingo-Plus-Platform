from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('Courses.urls', namespace="Courses")),
    path('profiles/', include('Profiles.urls', namespace="Profiles")),
    path('accounts/', include('Accounts.urls', namespace="Accounts")),
    path('users/', include('Users.urls', namespace="Users")),
    path('courses/', include('Courses.urls')),
    path('tickets/', include('Tickets.urls')),
    path('blogs/', include('Blogs.urls')),
    path('auth/', include('Authentication.urls', namespace="authentication")),
    path('articles/', include('Articles.urls')),
    path('books/', include('Books.urls')),
    path('podcasts/', include('Podcasts.urls')),
    path('subscriptions/', include('Subscriptions.urls')),
    path('carts/', include('Carts.urls')),
    path('orders/', include('Orders.urls')),
    path('coupons/', include('Coupons.urls')),
    path('wallets/', include('Wallets.urls')),
    path('discounts/', include('Discounts.urls')),
    # ckeditor_editor url
    path('ckeditor/', include('ckeditor_uploader.urls')),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
