from datetime import datetime
from django.db import models

# -------------------------
# Table des utilisateurs
# -------------------------
class Utilisateur(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('super', 'Super Administrateur'),
        ('enseignant', 'Enseignant'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    # Nouveaux champs
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"



# -------------------------
# Table des élèves
# -------------------------
class Etudiant(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    ]

    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="actif")
    photo = models.ImageField(upload_to='photos_etudiants/', null=True, blank=True)  # Nouveau champ

    def save(self, *args, **kwargs):
        if not self.matricule:
            annee = datetime.now().year
            self.matricule = f"{self.nom[:2].upper()}{self.prenom[:2].upper()}{self.date_naissance.strftime('%d%m%Y')}{str(annee)[-2:]}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"



# -------------------------
# Table des logiciels
# -------------------------
DUREE_CHOICES = [
    ('1semaine', '1 semaine'),
    ('2semaines', '2 semaines'),
    ('3semaines', '3 semaines'),
    ('1mois', '1 mois'),
    ('2mois', '2 mois'),
    ('3mois', '3 mois'),
    ('indefini', 'Indéfini'),
]

class Logiciel(models.Model):
    code_logiciel = models.CharField(max_length=20, unique=True, blank=True)
    nom = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    # Nouvelle durée sous forme de texte
    duree = models.CharField(max_length=20, choices=DUREE_CHOICES, default='indefini')
    
    # Durée en jours pour saisie personnalisée
    duree_jours = models.IntegerField(null=True, blank=True)
    
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Génération automatique du code si vide
        if not self.code_logiciel:
            nom_logiciel = self.nom[:2].upper() if self.nom else "XX"
            # Ici on peut mettre des lettres par défaut si aucun utilisateur
            self.code_logiciel = f"{nom_logiciel}{datetime.now().year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


# -------------------------
# Table des inscriptions
# -------------------------
class Inscription(models.Model):
    STATUT_CHOICES = [
        ('inscrit', 'Inscrit'),
        ('termine', 'Terminé'),
        ('abandon', 'Abandon'),
    ]

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE,related_name="inscriptions")
    logiciel = models.ForeignKey(Logiciel, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="inscrit")
    prix_inscription = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('etudiant', 'logiciel')

    def save(self, *args, **kwargs):
        # Si pas encore défini, récupérer le prix du logiciel
        if not self.prix_inscription and self.logiciel:
            self.prix_inscription = self.logiciel.prix
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.etudiant} -> {self.logiciel} ({self.prix_inscription} GNF)"


# -------------------------
# Table des emplois du temps
# -------------------------
class EmploiTemps(models.Model):
    JOURS_CHOICES = [
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
        ('dimanche', 'Dimanche'),
    ]
    logiciel = models.ForeignKey(Logiciel, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    jour_semaine = models.CharField(max_length=20, choices=JOURS_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.logiciel} ({self.jour_semaine})"


# -------------------------
# Paiement des élèves
# -------------------------
class Paiement(models.Model):
    MODE_CHOICES = [
        ('cash', 'Espèces'),
        ('mobile_money', 'Mobile Money'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement bancaire'),
    ]

    inscription = models.ForeignKey("Inscription", on_delete=models.CASCADE, related_name="paiements")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)  # montant attendu
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # cumul payé
    date_creation = models.DateTimeField(auto_now_add=True)
    est_solde = models.BooleanField(default=False)

    def __str__(self):
        return f"Paiement de {self.inscription.eleve} pour {self.inscription.matiere}"

    def reste_a_payer(self):
        return self.montant_total - self.montant_paye


# -------------------------
# Tranches de paiement
# -------------------------
class TranchePaiement(models.Model):
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name="tranches")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=20, choices=Paiement.MODE_CHOICES, default='cash')
    reference = models.CharField(max_length=100, null=True, blank=True)  # ex: numéro de reçu ou transaction

    def __str__(self):
        return f"Tranche {self.montant} - {self.paiement.inscription.eleve}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Met à jour le montant payé du paiement principal
        paiement = self.paiement
        paiement.montant_paye = sum([t.montant for t in paiement.tranches.all()])
        paiement.est_solde = paiement.montant_paye >= paiement.montant_total
        paiement.save()