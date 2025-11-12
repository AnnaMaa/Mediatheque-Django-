from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),  # ← page d’accueil = public
    path("biblio/", include("bibliothecaire.urls")),  # privé bibliothécaires
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
]
