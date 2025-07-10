from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('scrap', views.scrap, name='scrap'),
]