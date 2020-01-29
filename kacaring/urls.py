from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('index.urls')),
    path('', include('tbu.urls')),
    path('tur', include('ture.urls')),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
