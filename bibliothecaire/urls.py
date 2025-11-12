from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="biblio_dashboard"),
    path("membres/", views.liste_membres, name="biblio_membres"),
    path("medias/", views.liste_medias, name="biblio_medias"),
    path("emprunts/", views.liste_emprunts, name="biblio_emprunts"),

]
