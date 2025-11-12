from django.shortcuts import render
from .models import Livre, Dvd, Cd, JeuDePlateau
import logging


logger = logging.getLogger(__name__)

def creer_emprunt(request):
    logger.info(f"Nouvel emprunt par {request.user}")


def catalogue(request):
    ctx = {
        "livres": Livre.objects.all(),
        "dvds": Dvd.objects.all(),
        "cds": Cd.objects.all(),
        "jeux": JeuDePlateau.objects.all(),  # consultation uniquement
    }
    return render(request, "catalogue.html", ctx)
