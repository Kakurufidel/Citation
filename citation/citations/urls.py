from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from .views import (
    RegisterView, LoginView, LogoutView,
    AddQuoteView, DeleteQuoteView, QuoteListView, QuoteDetailView,
    AddCommentView, AddRatingView, AddFavoriteView, RemoveFavoriteView, ReportQuoteView
)

# URLs pour les médias (fichiers multimédias)
urlpatterns = []

# Ajoutez les URLs pour les médias uniquement en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs principales avec prise en charge de la traduction
urlpatterns += i18n_patterns(
    # Interface d'administration
    path('admin/', admin.site.urls),

    ### URLs d'authentification ###
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    ### URLs pour les citations ###
    path('quotes/', QuoteListView.as_view(), name='quote_list'),
    path('quotes/add/', AddQuoteView.as_view(), name='add_quote'),
    path('quotes/<int:quote_id>/', QuoteDetailView.as_view(), name='quote_detail'),
    path('quotes/<int:quote_id>/delete/', DeleteQuoteView.as_view(), name='delete_quote'),

    ### URLs pour les commentaires ###
    path('quotes/<int:quote_id>/comment/', AddCommentView.as_view(), name='add_comment'),

    ### URLs pour les évaluations ###
    path('quotes/<int:quote_id>/rate/', AddRatingView.as_view(), name='add_rating'),

    ### URLs pour les favoris ###
    path('quotes/<int:quote_id>/favorite/', AddFavoriteView.as_view(), name='add_favorite'),
    path('quotes/<int:quote_id>/unfavorite/', RemoveFavoriteView.as_view(), name='remove_favorite'),

    ### URLs pour les signalements ###
    path('quotes/<int:quote_id>/report/', ReportQuoteView.as_view(), name='report_quote'),

    # Inclure les URLs de l'application
    path('', include('votre_app.urls')),
)