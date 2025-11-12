# 📚 Projet Django — Gestion de Médiathèque

Ce projet a été développé dans le cadre du devoir **"Programmer orienté-objet avec Python"**.  
L’objectif est de créer un **logiciel de gestion de médiathèque** en respectant les principes de la **programmation orientée objet (POO)** et en utilisant le framework **Django**.

---

## 🚀 Fonctionnalités principales

### 🎓 Application Bibliothécaire (accès restreint)
- Création, modification et suppression de **membres**
- Gestion des **livres, CD, DVD et jeux de plateau**
- Création et suivi des **emprunts**
- Retour des médias empruntés (remise automatique en disponible)
- Règles métier intégrées :
  - Un membre ne peut pas emprunter plus de **3 médias**
  - Un emprunt dure **1 semaine**
  - Un membre en retard ne peut plus emprunter
  - Les jeux de plateau ne sont **pas empruntables**

### 👥 Application Publique (consultation)
- Consultation du **catalogue complet** (livres, CD, DVD, jeux)
- Affichage du statut (disponible / emprunté)

---

## 🧩 Structure du projet

mediatheque/
│
├── manage.py
├── mediatheque/ ← Configuration principale Django
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── catalog/ ← Application publique (consultation)
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│ │ └── catalogue.html
│ └── tests.py
│
├── bibliothecaire/ ← Application interne (bibliothécaires)
│ ├── views.py
│ ├── urls.py
│ └── templates/
│ └── bibliothecaire/
│ ├── dashboard.html
│ ├── liste_membres.html
│ ├── liste_medias.html
│ └── liste_emprunts.html
│
├── catalog/fixtures/ ← Données de démonstration
│ └── demo.json
│
├── logs/ ← Fichiers journaux (logging)
│ └── mediatheque.log
│
├── requirements.txt
└── README.md
---

## 🧠 Contraintes et principes POO

- **Héritage :**
  - Classe abstraite `Media`
  - Sous-classes `Livre`, `Dvd`, `Cd`
  - Classe indépendante `JeuDePlateau`
- **Encapsulation :**
  - Accès contrôlé aux emprunts d’un membre via des méthodes (`peut_emprunter`, `a_un_retard`, `emprunts_actifs`)
- **Polymorphisme :**
  - Les différents types de médias (`Livre`, `Cd`, `Dvd`) sont manipulés de manière uniforme via la classe parente `Media`.

---

## 🧰 Installation & exécution

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/AnnaMaa/Mediatheque-Django-.git
cd Mediatheque-Django-
2️⃣ Créer un environnement virtuel
py -m venv .venv
.\.venv\Scripts\activate

3️⃣ Installer les dépendances
pip install -r requirements.txt

4️⃣ Initialiser la base de données
python manage.py migrate
python manage.py loaddata catalog/fixtures/demo.json

5️⃣ Créer un superutilisateur
python manage.py createsuperuser

6️⃣ Lancer le serveur
python manage.py runserver


Application publique : http://127.0.0.1:8000/

Espace bibliothécaire : http://127.0.0.1:8000/biblio/

Administration Django : http://127.0.0.1:8000/admin/

🧪 Tests unitaires

Le projet inclut 6 tests automatisés vérifiant les règles métier :

pytest -q


✅ Création de membres et médias
✅ Création / retour d’emprunts
✅ Blocage des retards
✅ Limite de 3 emprunts

📝 Logs

Les actions importantes sont journalisées dans logs/mediatheque.log :

Création d’un emprunt

Retour d’un média

Tentative d’emprunt refusée (quota, retard, indisponibilité)

🗃️ Données de démonstration

Tu peux charger une base d’exemple avec :

python manage.py loaddata catalog/fixtures/demo.json


Elle contient :

5 livres

5 CD

5 DVD

2 membres

1 jeu de plateau

🧑‍💻 Auteur

👩‍💻 Anaïs
Projet réalisé dans le cadre du module Programmer orienté-objet avec Python.