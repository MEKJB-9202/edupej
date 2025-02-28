from django.urls import path
from . import views
from .views import edit_mentor_profile
urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # Formateurs
    path('formateur/dashboard/', views.formateur_dashboard, name='formateur_dashboard'),
    path('formateur/cours/ajouter/', views.ajouter_cours, name='ajouter_cours'),
    path('formateur/cours/modifier/<int:cours_id>/', views.modifier_cours, name='modifier_cours'),
    path('formateur/cours/supprimer/<int:cours_id>/', views.supprimer_cours, name='supprimer_cours'),
    
    # Apprenants
    path('apprenant/dashboard/', views.apprenant_dashboard, name='apprenant_dashboard'),
    path('apprenant/cours/<int:cours_id>/', views.detail_cours, name='detail_cours'),
    path('apprenant/quiz/<int:quiz_id>/', views.passer_quiz, name='passer_quiz'),
    
    # Parents
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),

    # Entretiens mentor/apprenant
    path('entretiens/', views.liste_entretiens, name='liste_entretiens'),
    path('entretiens/planifier/', views.planifier_entretien, name='planifier_entretien'),
    path('cours/', views.liste_cours, name='cours_liste'),
    
    # Gestion des notes
    path('apprenant/notes/', views.consulter_notes, name='consulter_notes'),
    path('mentor/dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('mentor/dashboard/', views.mentor_dashboard, name='mentor_dashboard'), 
    path('mentor/edit/', edit_mentor_profile, name='edit_mentor_profile'),
    ]
