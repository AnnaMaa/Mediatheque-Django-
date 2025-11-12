from django.test import TestCase


import pytest
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import (
    Membre, Livre, Dvd, Cd, Emprunt,
    DUREE_EMPRUNT_JOURS, MAX_EMPRUNTS_PAR_MEMBRE,
)

pytestmark = pytest.mark.django_db


def test_creer_membre():
    m = Membre.objects.create(nom="Alice", email="alice@test.com")
    assert Membre.objects.count() == 1
    assert m.nom == "Alice"


def test_creer_media_livre_cd_dvd():
    l = Livre.objects.create(titre="Le Petit Prince", auteur="Saint-Exupéry")
    c = Cd.objects.create(titre="Thriller", artiste="Michael Jackson")
    d = Dvd.objects.create(titre="Matrix", realisateur="Wachowski")
    assert l.disponible is True
    assert c.disponible is True
    assert d.disponible is True


def test_emprunt_ok_rend_media_indisponible():
    m = Membre.objects.create(nom="Bob", email="bob@test.com")
    l = Livre.objects.create(titre="1984", auteur="George Orwell")
    e = Emprunt.objects.create(membre=m, livre=l)  # création OK
    l.refresh_from_db()
    assert e.pk is not None
    assert l.disponible is False  # le save() de Emprunt a bien mis à jour


def test_retour_emprunt_rend_media_disponible():
    m = Membre.objects.create(nom="Carol", email="carol@test.com")
    l = Livre.objects.create(titre="HP1", auteur="Rowling")
    e = Emprunt.objects.create(membre=m, livre=l)
    # retour
    e.date_retour = timezone.now()
    e.save()
    l.refresh_from_db()
    assert l.disponible is True


def test_quota_3_emprunts_max():
    m = Membre.objects.create(nom="Dan", email="dan@test.com")
    livres = [Livre.objects.create(titre=f"L{i}", auteur="X") for i in range(MAX_EMPRUNTS_PAR_MEMBRE + 1)]
    # 3 emprunts autorisés
    for i in range(MAX_EMPRUNTS_PAR_MEMBRE):
        Emprunt.objects.create(membre=m, livre=livres[i])

    # 4e emprunt → doit être refusé par la validation
    e = Emprunt(membre=m, livre=livres[-1])
    with pytest.raises(ValidationError):
        e.full_clean()  # on force l'appel à clean()
    # et bien sûr on ne sauvegarde pas


def test_retard_bloque_nouvel_emprunt():
    m = Membre.objects.create(nom="Eve", email="eve@test.com")
    l1 = Livre.objects.create(titre="Ancien", auteur="Y")
    e1 = Emprunt.objects.create(membre=m, livre=l1)
    # simuler un retard (> DUREE_EMPRUNT_JOURS)
    e1.date_emprunt = timezone.now() - timedelta(days=DUREE_EMPRUNT_JOURS + 1)
    e1.save()

    assert m.a_un_retard() is True

    l2 = Livre.objects.create(titre="Nouveau", auteur="Z")
    e2 = Emprunt(membre=m, livre=l2)
    with pytest.raises(ValidationError):
        e2.full_clean()


def test_media_indisponible_refuse_deuxieme_emprunt():
    l = Livre.objects.create(titre="Dispo unique", auteur="Auteur")
    m1 = Membre.objects.create(nom="Fay", email="fay@test.com")
    m2 = Membre.objects.create(nom="Gus", email="gus@test.com")

    Emprunt.objects.create(membre=m1, livre=l)  # rend le livre indisponible
    l.refresh_from_db()
    assert l.disponible is False

    # deuxième emprunt sur le même livre → refus
    e = Emprunt(membre=m2, livre=l)
    with pytest.raises(ValidationError):
        e.full_clean()
