from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateTur.as_view(), name='create_tur'),
    path('update/<int:pk>/', views.TurUpdate.as_view(), name='update_tur'),
]
