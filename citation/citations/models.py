from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

class BaseModel(models.Model):
    """
    Base model containing common fields for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Deleted At"))

    class Meta:
        abstract = True  # This model won't be created in the database


class Category(BaseModel):
    """
    Model for categorizing quotes (e.g., Inspiration, Humor, Philosophy).
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Category Name"),
        help_text=_("The name of the category (e.g., Inspiration, Humor, etc.).")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Category Description"),
        help_text=_("A description of the category.")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Indicates whether the category is active or not.")
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("A unique identifier for the category's URL.")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']


class Quote(BaseModel):
    """
    Main model for storing quotes.
    """
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]

    text = models.TextField(
        verbose_name=_("Quote Text"),
        validators=[MinLengthValidator(10)],
        help_text=_("The text of the quote (at least 10 characters).")
    )
    author = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Quote Author"),
        help_text=_("The author of the quote (optional).")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Category"),
        help_text=_("The category to which the quote belongs.")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("User"),
        help_text=_("The user who created the quote.")
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_("Status"),
        help_text=_("The status of the quote (e.g., Draft, Published, Archived).")
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Views"),
        help_text=_("The number of times the quote has been viewed.")
    )
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Likes"),
        help_text=_("The number of likes the quote has received.")
    )
    featured = models.BooleanField(
        default=False,
        verbose_name=_("Featured"),
        help_text=_("Indicates whether the quote is featured.")
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Tags"),
        help_text=_("Keywords to make the quote easier to find (comma-separated).")
    )

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")
        ordering = ['-created_at']

    def publish(self):
        """
        Publish the quote by changing its status to 'published'.
        """
        self.status = 'published'
        self.save()

    def archive(self):
        """
        Archive the quote by changing its status to 'archived'.
        """
        self.status = 'archived'
        self.save()

    def increment_views(self):
        """
        Increment the number of views for the quote.
        """
        self.views += 1
        self.save()

    def increment_likes(self):
        """
        Increment the number of likes for the quote.
        """
        self.likes += 1
        self.save()