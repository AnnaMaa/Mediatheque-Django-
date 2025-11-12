
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from catalog.models import Membre, Livre, Dvd, Cd, JeuDePlateau, Emprunt

# Vérifie si l'utilisateur est staff (bibliothécaire)
def est_bibliothecaire(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(est_bibliothecaire)
def dashboard(request):
    return render(request, "bibliothecaire/dashboard.html")

@login_required
@user_passes_test(est_bibliothecaire)
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, "bibliothecaire/liste_membres.html", {"membres": membres})

@login_required
@user_passes_test(est_bibliothecaire)
def liste_medias(request):
    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    jeux = JeuDePlateau.objects.all()
    return render(request, "bibliothecaire/liste_medias.html", {
        "livres": livres,
        "dvds": dvds,
        "cds": cds,
        "jeux": jeux
    })

@login_required
@user_passes_test(est_bibliothecaire)
def liste_emprunts(request):
    emprunts = Emprunt.objects.all()
    return render(request, "bibliothecaire/liste_emprunts.html", {"emprunts": emprunts})
