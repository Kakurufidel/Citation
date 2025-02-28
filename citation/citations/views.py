from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import Quote, Category, Tag, Comment, Rating, Favorite, Report
from .forms import UserCreationForm, UserLoginForm, QuoteForm, CommentForm, RatingForm, ReportForm

### Vues d'authentification ###

class RegisterView(View):
    """
    Vue pour l'inscription des utilisateurs.
    """
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Votre compte a été créé avec succès.'))
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    """
    Vue pour la connexion des utilisateurs.
    """
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Vous êtes maintenant connecté.'))
                return redirect('quote_list')
            else:
                messages.error(request, _('Nom d’utilisateur ou mot de passe incorrect.'))
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    """
    Vue pour la déconnexion des utilisateurs.
    """
    def get(self, request):
        logout(request)
        messages.success(request, _('Vous avez été déconnecté.'))
        return redirect('login')

### Vues pour les citations ###

class AddQuoteView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vue pour ajouter une citation (réservée aux superutilisateurs).
    """
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = QuoteForm()
        return render(request, 'add_quote.html', {'form': form})

    def post(self, request):
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            form.save_m2m()  # Pour enregistrer les tags (ManyToMany)
            messages.success(request, _('La citation a été ajoutée avec succès.'))
            return redirect('quote_list')
        return render(request, 'add_quote.html', {'form': form})


class DeleteQuoteView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vue pour supprimer une citation (réservée aux administrateurs).
    """
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        quote.delete()
        messages.success(request, _('La citation a été supprimée avec succès.'))
        return redirect('quote_list')


class QuoteListView(View):
    """
    Vue pour afficher la liste des citations.
    """
    def get(self, request):
        quotes = Quote.objects.all()
        return render(request, 'quote_list.html', {'quotes': quotes})


class QuoteDetailView(View):
    """
    Vue pour afficher les détails d'une citation.
    """
    def get(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        comments = Comment.objects.filter(quote=quote)
        ratings = Rating.objects.filter(quote=quote)
        return render(request, 'quote_detail.html', {'quote': quote, 'comments': comments, 'ratings': ratings})

### Vues pour les commentaires ###

class AddCommentView(LoginRequiredMixin, View):
    """
    Vue pour ajouter un commentaire à une citation.
    """
    login_url = reverse_lazy('login')

    def get(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        form = CommentForm()
        return render(request, 'add_comment.html', {'form': form, 'quote': quote})

    def post(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.quote = quote
            comment.user = request.user
            comment.save()
            messages.success(request, _('Votre commentaire a été ajouté avec succès.'))
            return redirect('quote_detail', quote_id=quote.id)
        return render(request, 'add_comment.html', {'form': form, 'quote': quote})

### Vues pour les évaluations ###

class AddRatingView(LoginRequiredMixin, View):
    """
    Vue pour ajouter une évaluation à une citation.
    """
    login_url = reverse_lazy('login')

    def get(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        form = RatingForm()
        return render(request, 'add_rating.html', {'form': form, 'quote': quote})

    def post(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(quote=quote, user=request.user)
            rating.score = form.cleaned_data['score']
            rating.save()
            messages.success(request, _('Votre évaluation a été enregistrée avec succès.'))
            return redirect('quote_detail', quote_id=quote.id)
        return render(request, 'add_rating.html', {'form': form, 'quote': quote})

### Vues pour les favoris ###

class AddFavoriteView(LoginRequiredMixin, View):
    """
    Vue pour ajouter une citation aux favoris.
    """
    login_url = reverse_lazy('login')

    def get(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        Favorite.objects.get_or_create(user=request.user, quote=quote)
        messages.success(request, _('La citation a été ajoutée à vos favoris.'))
        return redirect('quote_detail', quote_id=quote.id)


class RemoveFavoriteView(LoginRequiredMixin, View):
    """
    Vue pour retirer une citation des favoris.
    """
    login_url = reverse_lazy('login')

    def get(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        Favorite.objects.filter(user=request.user, quote=quote).delete()
        messages.success(request, _('La citation a été retirée de vos favoris.'))
        return redirect('quote_detail', quote_id=quote.id)

### Vues pour les signalements ###

class ReportQuoteView(LoginRequiredMixin, View):
    """
    Vue pour signaler une citation comme inappropriée.
    """
    login_url = reverse_lazy('login')

    def get(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        form = ReportForm()
        return render(request, 'report_quote.html', {'form': form, 'quote': quote})

    def post(self, request, quote_id):
        quote = get_object_or_404(Quote, id=quote_id)
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.quote = quote
            report.user = request.user
            report.save()
            messages.success(request, _('La citation a été signalée avec succès.'))
            return redirect('quote_detail', quote_id=quote.id)
        return render(request, 'report_quote.html', {'form': form, 'quote': quote})