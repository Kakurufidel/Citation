from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator

class BaseModel(models.Model):
    """
    Classe de base contenant les champs communs à tous les modèles.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Deleted At"))

    class Meta:
        abstract = True


class Category(BaseModel):
    """
    Modèle pour catégoriser les citations (ex: Inspiration, Humor, Philosophy, etc.).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Category Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']


class Tag(BaseModel):
    """
    Modèle pour les tags associés aux citations.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Tag Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']


class Quote(BaseModel):
    """
    Modèle principal pour stocker les citations.
    """
    text = models.TextField(verbose_name=_("Quote Text"))
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Quote Author"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Category"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("User"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")
        ordering = ['-created_at']

    def get_short_text(self, length=50):
        """
        Retourne une version raccourcie du texte de la citation.
        """
        if len(self.text) > length:
            return self.text[:length] + "..."
        return self.text


class Comment(BaseModel):
    """
    Modèle pour les commentaires sur les citations.
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Quote"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    text = models.TextField(verbose_name=_("Comment Text"))
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name=_("Parent Comment"))

    def __str__(self):
        return f"Comment by {self.user.username} on {self.quote}"

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']


class Rating(BaseModel):
    """
    Modèle pour les évaluations des citations par les utilisateurs.
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='ratings', verbose_name=_("Quote"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    score = models.PositiveSmallIntegerField(
        validators=[MinLengthValidator(1), MaxLengthValidator(5)],
        verbose_name=_("Rating Score")
    )

    def __str__(self):
        return f"Rating {self.score} by {self.user.username} on {self.quote}"

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = ('quote', 'user')  # Un utilisateur ne peut noter une citation qu'une seule fois.


class Favorite(BaseModel):
    """
    Modèle pour les citations favorites des utilisateurs.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name=_("User"))
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='favorited_by', verbose_name=_("Quote"))

    def __str__(self):
        return f"{self.user.username} favorited {self.quote}"

    class Meta:
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")
        unique_together = ('user', 'quote')  # Un utilisateur ne peut ajouter une citation qu'une seule fois aux favoris.


class Report(BaseModel):
    """
    Modèle pour signaler des citations inappropriées.
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='reports', verbose_name=_("Quote"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    reason = models.TextField(verbose_name=_("Report Reason"))
    resolved = models.BooleanField(default=False, verbose_name=_("Resolved"))

    def __str__(self):
        return f"Report by {self.user.username} on {self.quote}"

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ['-created_at']