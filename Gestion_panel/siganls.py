# # Gestion_panel/signals.py
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from Gestion_panel.models import Utilisateur
# from django.contrib.auth.hashers import make_password

# @receiver(post_migrate)
# def create_super_user(sender, **kwargs):
#     if sender.name == 'Gestion_panel':
#         if not Utilisateur.objects.filter(email="admin@example.com").exists():
#             Utilisateur.objects.create(
#                 nom="Admin",
#                 prenom="Super",
#                 email="admin@gmail.com",
#                 mot_de_passe=make_password("1234"),
#                 role="super",
#                 actif=True,
#                 adresse="Admin Address",
#                 telephone="1234567890",
#             )
#             print("Super utilisateur créé avec succès !")
