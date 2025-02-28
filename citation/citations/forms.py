from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Quote, Comment, Rating, Report

### Formulaires d'authentification ###

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé avec des labels traduits.
    """
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': _('Nom d’utilisateur'),
            'password1': _('Mot de passe'),
            'password2': _('Confirmation du mot de passe'),
        }
        help_texts = {
            'username': _('Requis. 150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.'),
            'password1': _('Votre mot de passe doit contenir au moins 8 caractères.'),
            'password2': _('Entrez le même mot de passe que précédemment, pour vérification.'),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé avec des labels traduits.
    """
    username = forms.CharField(label=_('Nom d’utilisateur'))
    password = forms.CharField(label=_('Mot de passe'), widget=forms.PasswordInput)

### Formulaires pour les citations ###

class QuoteForm(forms.ModelForm):
    """
    Formulaire pour ajouter ou modifier une citation.
    """
    class Meta:
        model = Quote
        fields = ['text', 'author', 'category', 'tags']
        labels = {
            'text': _('Texte de la citation'),
            'author': _('Auteur'),
            'category': _('Catégorie'),
            'tags': _('Tags'),
        }
        help_texts = {
            'text': _('Entrez le texte de la citation.'),
            'author': _('Entrez le nom de l’auteur (optionnel).'),
            'category': _('Sélectionnez une catégorie pour la citation.'),
            'tags': _('Sélectionnez ou créez des tags pour la citation.'),
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

### Formulaires pour les commentaires ###

class CommentForm(forms.ModelForm):
    """
    Formulaire pour ajouter un commentaire à une citation.
    """
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': _('Commentaire'),
        }
        help_texts = {
            'text': _('Écrivez votre commentaire ici.'),
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

### Formulaires pour les évaluations ###

class RatingForm(forms.ModelForm):
    """
    Formulaire pour évaluer une citation.
    """
    class Meta:
        model = Rating
        fields = ['score']
        labels = {
            'score': _('Note'),
        }
        help_texts = {
            'score': _('Donnez une note entre 1 et 5.'),
        }
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

### Formulaires pour les signalements ###

class ReportForm(forms.ModelForm):
    """
    Formulaire pour signaler une citation comme inappropriée.
    """
    class Meta:
        model = Report
        fields = ['reason']
        labels = {
            'reason': _('Raison du signalement'),
        }
        help_texts = {
            'reason': _('Expliquez pourquoi vous signalez cette citation.'),
        }
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }