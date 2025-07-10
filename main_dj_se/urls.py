from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrap, name='scrap'),
]