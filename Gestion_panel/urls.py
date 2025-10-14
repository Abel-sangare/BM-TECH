from django.urls import path
from django.conf.urls.static import static
from BMTech import settings
from . import views

# app_name = "B"  # 🔹 Change "monapp" par le nom de ton app

urlpatterns = [
    path('', views.home, name="index"),  # page d'accueil de l'app
    path('login/', views.login, name="login"),  # page d'accueil de l'app


    path('etudiants/', views.etudiants, name="etudiants"),  # page d'accueil de l'app
    path('inscrire_etudiant/', views.inscrire_etudiant, name="inscrire_etudiant"),  # page d'accueil de l'app

    path('utilisateurs/', views.utilisateurs, name="utilisateurs"),  # page d'accueil de l'app
    path('creer_utilisateur/', views.creer_utilisateur, name="creer_utilisateur"),  # page d'accueil de l'app
    path('supprimer_utilisateur/<int:user_id>/', views.supprimer_utilisateur, name="supprimer_utilisateur"),  # page d'accueil de l'app
    path('desactiver_utilisateur/<int:user_id>/', views.desactiver_utilisateur, name="desactiver_utilisateur"),  # page d'accueil de l'app
    path('reactiver_utilisateur/<int:user_id>/', views.reactiver_utilisateur, name="reactiver_utilisateur"),  # page d'accueil de l'app

    path('logiciels/', views.logiciels, name="logiciels"),  # page d'accueil de l'app
    path('gestion_logiciel/', views.gestion_logiciel, name="gestion_logiciel"),  # page d'accueil de l'app
    path('gestion_logiciel/<int:logiciel_id>/', views.gestion_logiciel, name="modifier_logiciel"),
    path('supprimer_logiciel/<int:logiciel_id>/', views.supprimer_logiciel, name="supprimer_logiciel"),  # page d'accueil de l'app
    path('imprimer_programme/', views.imprimer_programme, name="imprimer_programme"),  # page d'accueil de l'app


    path('emploi/', views.emploi, name="emploi"),  # page d'accueil de l'app
    path('paiements/', views.paiements, name="paiements"),  # page d'accueil de l'app
    path('handler_connexion/', views.handler_connexion, name='handler_connexion'),
    path('logout/', views.deconnexion, name='logout'),
    path('profil/', views.profil, name='profil'),
    path('mise_a_jour_profil/', views.mise_a_jour_profil, name='mise_a_jour_profil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)