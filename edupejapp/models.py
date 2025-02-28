from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Modèle utilisateur personnalisé
class User(AbstractUser):
    ROLE_CHOICES = [
        ('apprenant', 'Apprenant'),
        ('parent', 'Parent'),
        ('mentor', 'Mentor'),
        ('formateur', 'Formateur')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    demande_validation = models.BooleanField(default=False)

    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, blank=True, 
        related_name='enfants', 
        limit_choices_to={'role': 'parent'}
    )

    mentor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='apprenants',
        limit_choices_to={'role': 'mentor'}
    )
    
    photo = models.ImageField(upload_to='photos_profil/', blank=True, null=True)
    specialite = models.CharField(max_length=255, blank=True, null=True, help_text="Spécialité du formateur")
    
    def get_available_mentors():
        return User.objects.filter(role='mentor')

    # Ajout de related_name pour éviter les conflits avec le modèle auth.User
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

    def __str__(self):
        return self.username

# Modèle pour les cours
class Cours(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    formateur = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'formateur'})
    duree = models.PositiveIntegerField(help_text="Durée en jours")  # Durée en jours de la formation

    def duree_videos(self):
        """
        Calcule la durée totale des vidéos associées à ce cours en minutes.
        """
        total_duree = sum(ressource.duree for ressource in self.ressources.filter(type_ressource='video'))
        return total_duree

    def __str__(self):
        return self.titre

class CoursRessource(models.Model):
    TYPE_CHOICES = [
        ('video', 'Vidéo'),
        ('pdf', 'PDF'),
        ('quiz', 'Quiz')
    ]
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='ressources')
    type_ressource = models.CharField(max_length=10, choices=TYPE_CHOICES)
    fichier = models.FileField(upload_to='cours_ressources/', blank=True, null=True)
    titre = models.CharField(max_length=255, blank=True, null=True)
    duree = models.PositiveIntegerField(blank=True, null=True, help_text="Durée de la vidéo en minutes, si applicable")  # Durée pour les vidéos

    def __str__(self):
        return f"{self.cours.titre} - {self.type_ressource}"
# Modèle pour suivre la progression de l'apprenant
class Progression(models.Model):
    apprenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'apprenant'})
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    termine = models.BooleanField(default=False)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.apprenant.username} - {self.cours.titre}"

# Modèle pour les entretiens mentor-apprenant
class Entretien(models.Model):
    apprenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entretiens_apprenant')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entretiens_mentor', limit_choices_to={'role': 'mentor'})
    date = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=[('prévu', 'Prévu'), ('terminé', 'Terminé')], default='prévu')

    def __str__(self):
        return f"Entretien {self.apprenant.username} avec {self.mentor.username} le {self.date}"
# Modèle pour les quiz
class Quiz(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='quiz')
    titre = models.CharField(max_length=255)

    def __str__(self):
        return f"Quiz de {self.cours.titre}"

# Modèle pour les questions du quiz
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    texte = models.TextField()
    choix1 = models.CharField(max_length=255)
    choix2 = models.CharField(max_length=255)
    choix3 = models.CharField(max_length=255)
    choix4 = models.CharField(max_length=255)
    bonne_reponse = models.CharField(max_length=255)

    def __str__(self):
        return self.texte

# Modèle pour les notes des apprenants
class Note(models.Model):
    apprenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'apprenant'})
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.apprenant.username} - {self.cours.titre} : {self.score}/100"
    
# edupejapp/models.py
from django.db import models

class Mentor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    photo = models.ImageField(upload_to='mentors/', null=True, blank=True)
    capacites = models.TextField(null=True, blank=True)
