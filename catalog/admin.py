
from django.contrib import admin
from catalog.models import Membre, Livre, Dvd, Cd, JeuDePlateau, Emprunt

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "bloque")
    search_fields = ("nom", "email")

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ("titre", "auteur", "disponible")
    search_fields = ("titre", "auteur")
    list_filter = ("disponible",)

@admin.register(Dvd)
class DvdAdmin(admin.ModelAdmin):
    list_display = ("titre", "realisateur", "disponible")
    search_fields = ("titre", "realisateur")
    list_filter = ("disponible",)

@admin.register(Cd)
class CdAdmin(admin.ModelAdmin):
    list_display = ("titre", "artiste", "disponible")
    search_fields = ("titre", "artiste")
    list_filter = ("disponible",)

@admin.register(JeuDePlateau)
class JeuDePlateauAdmin(admin.ModelAdmin):
    list_display = ("titre", "createur")

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ("membre", "media_obj", "date_emprunt", "date_retour")
    autocomplete_fields = ("membre", "livre", "dvd", "cd")
