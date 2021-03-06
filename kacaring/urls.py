from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('bookings/', include('bookings.urls')),
    path('email/', include('emailing.urls')),
    path('', include('index.urls')),
    path('', include('tbu.urls')),
    path('tur/', include('ture.urls')),
    path('oversigt/', include('accounts.urls')),
    path('user/', include('users.urls')),
    path('statistik/', include('statistik.urls')),
    path('admin/', admin.site.urls),
]
