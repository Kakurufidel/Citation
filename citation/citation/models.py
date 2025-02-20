from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BaseModel(models.Model):
    """
    Classe de base contenant les champs communs à tous les modèles.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deleted At")

    class Meta:
        abstract = True 


class Category(BaseModel):
    """
    Modèle pour catégoriser les citations (ex: Inspiration, Humor, Philosophy, etc.).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Category Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Quote(BaseModel):
    """
    Modèle principal pour stocker les citations.
    """
    text = models.TextField(verbose_name="Quote Text")
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name="Quote Author")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Category")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="User")

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ['-created_at']