from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User, Cours, Progression, Entretien
from django.contrib import messages
from .models import Quiz
from .forms import MentorForm
from .models import Mentor
def home(request):
    formateurs = User.objects.filter(role='formateur')
    return render(request, 'home.html', {'formateurs': formateurs})

def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Utilisation de .get() pour éviter une erreur
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not username or not email or not password or not role:
            messages.error(request, 'Tous les champs sont obligatoires.')
            return render(request, 'inscription.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Si le modèle User personnalisé a un champ `role`, il faut l'affecter et sauvegarder
        if hasattr(user, 'role'):
            user.role = role

        if role == 'mentor':
            apprenant_id = request.POST.get('mentor_apprenant')
            if apprenant_id:
                user.parent_id = apprenant_id  # Vérifie si `parent_id` existe dans ton modèle personnalisé

        elif role == 'parent':
            enfant_id = request.POST.get('parent_apprenant')
            if enfant_id:
                user.parent_id = enfant_id  # Vérifie aussi l'existence de `parent_id` ici

        user.save()
        messages.success(request, 'Inscription réussie, vous pouvez vous connecter !')
        return redirect('connexion')

    return render(request, 'inscription.html')

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Identifiants invalides')
    return render(request, 'connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('home')

@login_required
def formateur_dashboard(request):
    if request.user.role != 'formateur':
        return redirect('home')
    cours = Cours.objects.filter(formateur=request.user)
    return render(request, 'formateur_dashboard.html', {'cours': cours})

@login_required
def ajouter_cours(request):
    if request.user.role != 'formateur':
        return redirect('home')
    if request.method == 'POST':
        titre = request.POST['titre']
        description = request.POST['description']
        duree = request.POST['duree']
        Cours.objects.create(titre=titre, description=description, duree=duree, formateur=request.user)
        messages.success(request, 'Cours ajouté avec succès !')
        return redirect('formateur_dashboard')
    return render(request, 'ajouter_cours.html')
def modifier_cours(request, cours_id):
    cours = get_object_or_404(Cours, pk=cours_id)

    if request.method == 'POST':
        # Ajoutez ici la logique pour traiter les données du formulaire
        # Par exemple : cours.titre = request.POST.get('titre')
        cours.save()
        return redirect('nom_de_la_vue_de_redirection')  # Remplacez par le nom de la vue vers laquelle rediriger après la modification
    
    return render(request, 'modifier_cours.html', {'cours': cours})
@login_required
def apprenant_dashboard(request):
    if request.user.role != 'apprenant':
        return redirect('home')
    progression = Progression.objects.filter(apprenant=request.user)
    return render(request, 'apprenant_dashboard.html', {'progression': progression})

@login_required
def parent_dashboard(request):
    if request.user.role != 'parent':
        return redirect('home')
    enfants = request.user.enfants.all()
    return render(request, 'parent_dashboard.html', {'enfants': enfants})

@login_required
def liste_entretiens(request):
    if request.user.role not in ['apprenant', 'mentor']:
        return redirect('home')
    entretiens = Entretien.objects.filter(apprenant=request.user) if request.user.role == 'apprenant' else Entretien.objects.filter(mentor=request.user)
    return render(request, 'entretiens.html', {'entretiens': entretiens})

@login_required
@login_required
def mentor_dashboard(request):
    if request.user.role != 'mentor':
        return redirect('home')
    
    # Récupère les apprenants du mentor
    apprenants = request.user.apprenants.all()
    
    # Récupère tous les entretiens des apprenants du mentor
    entretiens = Entretien.objects.filter(mentor=request.user)
    
    return render(request, 'mentor_dashboard.html', {'apprenants': apprenants, 'entretiens': entretiens})

def supprimer_cours(request, cours_id):
    cours = get_object_or_404(Cours, pk=cours_id)
    
    if request.method == 'POST':
        cours.delete()  # Supprime le cours
        return redirect('nom_de_la_vue_de_redirection')  # Remplacez par la vue vers laquelle vous souhaitez rediriger

    # Si ce n'est pas un POST, vous pouvez rendre une page de confirmation de suppression, par exemple.
    return render(request, 'confirmation_supprimer_cours.html', {'cours': cours})

def detail_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    return render(request, 'detail_cours.html', {'cours': cours})


def passer_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Ajoutez ici la logique pour traiter le quiz, par exemple afficher les questions et gérer les réponses
    return render(request, 'passer_quiz.html', {'quiz': quiz})

def planifier_entretien(request):
    # Ajoutez ici la logique pour planifier un entretien, par exemple, afficher un formulaire.
    return render(request, 'planifier_entretien.html')

def consulter_notes(request):
    # Ajoutez ici la logique pour afficher les notes de l'apprenant
    return render(request, 'consulter_notes.html')

def liste_cours(request):
    cours = Cours.objects.all()
    return render(request, 'cours/liste_cours.html', {'cours': cours})



def edit_mentor_profile(request):
    mentor = User.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        form = MentorForm(request.POST, request.FILES, instance=mentor)
        if form.is_valid():
            form.save()
            return redirect('mentor_profile')  # Redirige vers la page de profil
    
    else:
        form = MentorForm(instance=mentor)

    return render(request, 'mentors/edit_profile.html', {'form': form})

def liste_mentors(request):
    mentors = User.objects.filter(role='mentor')
    return render(request, 'mentors/liste.html', {'mentors': mentors})