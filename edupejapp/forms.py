from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Mentor
class InscriptionForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    parent = forms.ModelChoiceField(queryset=User.objects.filter(role='parent'), required=False, empty_label="Choisir un parent (si applicable)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'parent']

class ConnexionForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    mentor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='mentor'),
        required=False,
        empty_label="Choisir un mentor (optionnel)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'parent', 'mentor']

from django import forms


class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ['photo', 'capacites']
        widgets = {
            'capacites': forms.CheckboxSelectMultiple
        }