@echo off
cd /d C:\Users\anais\mediatheque

echo === Activation de l'environnement virtuel ===
call .venv\Scripts\activate

echo === Lancement du serveur Django ===
python manage.py runserver

pause
