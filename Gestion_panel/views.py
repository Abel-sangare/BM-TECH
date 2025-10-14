import datetime
from datetime import datetime
from time import timezone
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password, check_password

from Gestion_panel.models import Etudiant, Inscription, Logiciel, Utilisateur


def home(request):
    return render(request, 'AdminPanel.html')



def login(request):
    return render(request, 'login.html')

def handler_connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect.")
            return redirect('login')

        # Vérification du mot de passe (crypté)
        if not check_password(password, user.mot_de_passe):
            messages.error(request, "Email ou mot de passe incorrect.1234")
            return redirect('login')

        # Vérification du statut actif
        if not user.actif:
            messages.error(request, "Votre compte est inactif. Contactez l'administrateur.")
            return redirect('login')

        # Enregistrer l'utilisateur dans la session
        request.session['user_id'] = user.id
        request.session['user_role'] = user.role
        request.session['user_nom'] = user.nom

        messages.success(request, f"Bienvenue {user.nom} {user.prenom} !")
        return redirect('index')  # redirection vers un seul dashboard commun

    return render(request, 'login.html')

#def create_super_utilisateur(request):

    # Créer le super administrateur
    super_admin = Utilisateur.objects.create(
        nom='Admin',
        prenom='Super',
        email='a@gmail.com',
        mot_de_passe=make_password('1234'),  # hash le mot de passe
        role='super',
        actif=True
    )

    messages.success(request, "Super administrateur créé avec succès.")
    return redirect('login')  # Toujours renvoyer un HttpResponse ou redirection

def deconnexion(request):
    # Supprime toutes les données de session de l'utilisateur
    request.session.flush()
    # Redirige vers la page de connexion
    return redirect('login')  # Assure-toi que 'login' correspond au nom de ta route

def profil(request):
    # On récupère l'utilisateur connecté via la session
    user_id = request.session.get("user_id")  # on suppose que tu stockes l'id à la connexion
    if not user_id:
        return redirect("login")  # pas connecté

    try:
        user = Utilisateur.objects.get(id=user_id)
    except Utilisateur.DoesNotExist:
        return redirect("login")

    if request.method == "POST":
        # Mise à jour des informations
        user.nom = request.POST.get("nom")
        user.prenom = request.POST.get("prenom")
        user.email = request.POST.get("email")
        user.telephone = request.POST.get("telephone")
        user.adresse = request.POST.get("adresse")
        mot_de_passe = request.POST.get("mot_de_passe")
        if mot_de_passe:
            user.mot_de_passe = mot_de_passe  # mettre en clair ou hasher selon ton système
        user.save()
        return redirect("profil")  # recharge la page après mise à jour

    return render(request, "profil.html", {"user": user})


def creer_utilisateur(request):
    # Vérification si connecté et si super admin
    if "user_id" not in request.session or request.session.get("user_role") != "super":
        return HttpResponseForbidden("Accès refusé !")

    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        mot_de_passe = request.POST.get("mot_de_passe")
        role = request.POST.get("role")
        telephone = request.POST.get("telephone")
        adresse = request.POST.get("adresse")

        # Vérifier si l'email existe déjà
        if Utilisateur.objects.filter(email=email).exists():
            return render(request, "creer_utilisateur.html", {
                "error": "Cet email existe déjà."
            })

        # Création de l'utilisateur
        Utilisateur.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=make_password(mot_de_passe),  # 🔐 mot de passe haché
            role=role,
            telephone=telephone,
            adresse=adresse,
            actif=True
        )
        messages.success(request, "Utilisateur créé avec succès !")
        return redirect("utilisateurs")  # tu peux rediriger vers une liste d'utilisateurs

    return render(request, "utilisateur.html")

def reactiver_utilisateur(request, user_id):
    if "user_id" not in request.session or request.session.get("user_role") != "super":
        return HttpResponseForbidden("Accès refusé !")

    user = get_object_or_404(Utilisateur, id=user_id)
    user.actif = True
    user.save()
    messages.success(request, f"Utilisateur {user.nom} {user.prenom} réactivé avec succès.")
    return redirect("utilisateurs")  # Redirection vers la liste


def desactiver_utilisateur(request, user_id):
    # Vérification si connecté et si super admin
    if "user_id" not in request.session or request.session.get("user_role") != "super":
        return HttpResponseForbidden("Accès refusé !")

    user = get_object_or_404(Utilisateur, id=user_id)

    # On désactive le compte
    user.actif = False
    user.save()
    messages.success(request, f"Utilisateur {user.nom} {user.prenom} désactivé avec succès.")
    return redirect("utilisateurs")  # Redirection vers la liste

def mise_a_jour_profil(request):
    if request.method == "POST":
        # Récupérer l'utilisateur connecté depuis la session
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')  # si non connecté

        utilisateur = get_object_or_404(Utilisateur, id=user_id)

        # Mettre à jour les champs depuis le formulaire
        utilisateur.nom = request.POST.get('nom', utilisateur.nom)
        utilisateur.prenom = request.POST.get('prenom', utilisateur.prenom)
        utilisateur.email = request.POST.get('email', utilisateur.email)
        utilisateur.telephone = request.POST.get('telephone', utilisateur.telephone)
        utilisateur.adresse = request.POST.get('adresse', utilisateur.adresse)

        mot_de_passe = request.POST.get('mot_de_passe')
        if mot_de_passe:
            utilisateur.mot_de_passe = mot_de_passe  # ou hash si nécessaire

        utilisateur.save()  # sauvegarde dans la base
        messages.success(request, "Profil mis à jour avec succès !")
        return redirect('profil')  # redirige vers la page profil après MAJ


def supprimer_utilisateur(request, user_id):
    # Vérification si connecté et si super admin
    if "user_id" not in request.session or request.session.get("user_role") != "super":
        return HttpResponseForbidden("Accès refusé !")

    user = get_object_or_404(Utilisateur, id=user_id)

    # Supprimer définitivement l'utilisateur
    user.delete()
    messages.success(request, f"Utilisateur {user.nom} {user.prenom} supprimé avec succès.")
    return redirect("utilisateurs")  # Redirection vers la liste

def etudiants(request):
    # Récupération de tous les étudiants
    etudiants = Etudiant.objects.all()

    # Récupération de tous les logiciels
    logiciels = Logiciel.objects.all()

    # Contexte pour le template
    context = {
        'etudiants': etudiants,
        'logiciels': logiciels,
    }
    return render(request, 'etudiants.html', context)

def inscrire_etudiant(request):
    logiciels = Logiciel.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        statut = request.POST.get('statut')
        logiciels_ids = request.POST.getlist('matieres')
        inscription_statut = request.POST.get('inscription_statut')

        # Gestion de la date de naissance
        date_naissance_str = request.POST.get('date_naissance')
        if date_naissance_str:
            try:
                from datetime import datetime
                date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
            except ValueError:
                date_naissance = None
        else:
            date_naissance = None

        # Gestion de la photo
        photo = request.FILES.get('photo')  # récupère le fichier uploadé

        # Création de l'étudiant
        etudiant = Etudiant(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            adresse=adresse,
            date_naissance=date_naissance,
            statut=statut,
            photo=photo  # assigne la photo
        )
        etudiant.save()

        # Inscription aux logiciels sélectionnés avec prix fixe
        for logiciel_id in logiciels_ids:
            try:
                logiciel = Logiciel.objects.get(id=logiciel_id)
                Inscription.objects.create(
                    etudiant=etudiant,
                    logiciel=logiciel,
                    statut=inscription_statut,
                    prix_inscription=25000  # prix fixe d'inscription
                )
            except Logiciel.DoesNotExist:
                continue  # ignore si le logiciel n'existe pas

        messages.success(request, "Étudiant inscrit avec succès !")
        return redirect('etudiants')

    return render(request, 'etudiants.html')


def logiciels(request):
    """
    Affiche tous les logiciels et gère la recherche par nom
    """
    query = request.GET.get('q', '')  # récupération du mot clé de recherche
    if query:
        logiciels = Logiciel.objects.filter(nom__icontains=query)
    else:
        logiciels = Logiciel.objects.all()
    
    # Vérification si on modifie un logiciel
    logiciel_id = request.GET.get('edit')
    logiciel = None
    if logiciel_id:
        logiciel = get_object_or_404(Logiciel, id=logiciel_id)
    
    context = {
        'logiciels': logiciels,   # <-- la liste de tous les logiciels pour le tableau
        'logiciel': logiciel,     # <-- logiciel à modifier pour le formulaire
        'query': query,           # <-- pour pré-remplir le champ de recherche si besoin
    }
    return render(request, 'logiciel.html', context)

def gestion_logiciel(request, logiciel_id=None):
    """
    Crée ou modifie un logiciel
    """
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        duree = request.POST.get('duree')  # 1 semaine, 2 semaines, etc.
        duree_jours = request.POST.get('duree_jours') or None  # optionnel
        prix = request.POST.get('prix') or 0.0

        # Création ou récupération pour modification
        if logiciel_id:
            logiciel = get_object_or_404(Logiciel, id=logiciel_id)
            logiciel.nom = nom
            logiciel.description = description
            logiciel.duree = duree
            logiciel.duree_jours = duree_jours
            logiciel.prix = prix
            messages.success(request, "Logiciel modifié avec succès !")
        else:
            # Génération automatique du code : deux premières lettres du logiciel + date en cours
            date_now = timezone.now().strftime('%Y%m%d')
            code_logiciel = f"{nom[:2].upper()}{date_now}"
            logiciel = Logiciel(
                code_logiciel=code_logiciel,
                nom=nom,
                description=description,
                duree=duree,
                duree_jours=duree_jours,
                prix=prix
            )
            messages.success(request, "Logiciel créé avec succès !")
        
        logiciel.save()
        return redirect('logiciels')

    # Pour GET ou autre, tu peux renvoyer le formulaire avec un logiciel existant si ID fourni
    if logiciel_id:
        logiciel = get_object_or_404(Logiciel, id=logiciel_id)
        context = {"logiciel": logiciel, "logiciels": Logiciel.objects.all()}
    else:
        context = {"logiciels": Logiciel.objects.all()}

    return render(request, 'logiciel.html', context)

def supprimer_logiciel(request, logiciel_id):
    """
    Supprime définitivement un logiciel
    """
    logiciel = get_object_or_404(Logiciel, id=logiciel_id)
    logiciel.delete()
    messages.success(request, "Logiciel supprimé avec succès !")
    return redirect('logiciels')

def imprimer_programme(request):
    # Récupération des logiciels, éventuellement filtrés par recherche
    search = request.GET.get('search', '')
    if search:
        logiciels = Logiciel.objects.filter(nom__icontains=search)
    else:
        logiciels = Logiciel.objects.all()

    # Charger le template HTML pour le PDF
    template_path = 'pdf/logiciel_pdf.html'
    context = {'logiciels': logiciels}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="logiciels.pdf"'

    # Générer le PDF
    template = get_template(template_path) # pyright: ignore[reportUndefinedVariable]
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response) # pyright: ignore[reportUndefinedVariable]
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF')
    return response

def emploi(request):
    return render(request, 'emploi.html')

def paiements(request):
    return render(request, 'paiement.html')

def utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'utilisateur.html', {'utilisateurs': utilisateurs})
