from django.db import models
from django.utils import timezone
from datetime import timedelta

MAX_EMPRUNTS_PAR_MEMBRE = 3
DUREE_EMPRUNT_JOURS = 7

class Membre(models.Model):
    nom = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)

    def emprunts_actifs(self):
        return self.emprunt_set.filter(date_retour__isnull=True)

    def a_un_retard(self):
        limite = timezone.now() - timedelta(days=DUREE_EMPRUNT_JOURS)
        return self.emprunts_actifs().filter(date_emprunt__lt=limite).exists()

    def peut_emprunter(self):
        if self.bloque or self.a_un_retard():
            return False
        return self.emprunts_actifs().count() < MAX_EMPRUNTS_PAR_MEMBRE

    def __str__(self):
        return self.nom

class Media(models.Model):
    titre = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.titre

class Livre(Media):
    auteur = models.CharField(max_length=120, blank=True, null=True)

class Dvd(Media):
    realisateur = models.CharField(max_length=120)

class Cd(Media):
    artiste = models.CharField(max_length=120)

class JeuDePlateau(models.Model):
    titre = models.CharField(max_length=200)
    createur = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.titre} (jeu de plateau)"

class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, null=True, blank=True, on_delete=models.PROTECT)
    dvd   = models.ForeignKey(Dvd,   null=True, blank=True, on_delete=models.PROTECT)
    cd    = models.ForeignKey(Cd,    null=True, blank=True, on_delete=models.PROTECT)
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour  = models.DateTimeField(null=True, blank=True)

    def media_obj(self):
        return self.livre or self.dvd or self.cd

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.membre.peut_emprunter():
            raise ValidationError("Le membre ne peut pas emprunter (bloqué, retard, ou quota atteint).")
        medias = [self.livre, self.dvd, self.cd]
        if sum(1 for x in medias if x) != 1:
            raise ValidationError("Choisir exactement un média (Livre OU Dvd OU Cd).")
        if self.media_obj() and not self.media_obj().disponible:
            raise ValidationError("Le média n'est pas disponible.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        media = self.media_obj()
        if media:
            if is_new:
                media.disponible = False
            elif self.date_retour is not None:
                media.disponible = True
            media.save()

    def est_en_retard(self):
        return not self.date_retour and self.date_emprunt < timezone.now() - timedelta(days=DUREE_EMPRUNT_JOURS)

    def __str__(self):
        return f"Emprunt {self.membre} -> {self.media_obj()}"
