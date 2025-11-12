from django.urls import path
from .views import catalogue

urlpatterns = [
    path("", catalogue, name="catalogue"),
]
