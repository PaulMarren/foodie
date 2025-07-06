from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Category(models.Model):
    """
    Represents a recipe category (e.g., Vegan, Italian, Dessert).
    """
    # Enforce unique category names
    name = models.CharField(max_length=50, unique=True)
    # URL-friendly version of name
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    # Optional description of the category
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"  # Plural name for admin interface

    def save(self, *args, **kwargs):
        """Automatically generate slug from name if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation"""
        return self.name


class Recipe(models.Model):
    """
    Main recipe model containing core information about a recipe.
    Related to Category, Equipment, Ingredient, and Instruction models.
    """
    title = models.CharField(max_length=200)  # Recipe title/name
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Recipe author
    prep_time = models.PositiveIntegerField()
    cook_time = models.PositiveIntegerField()
    total_time = models.PositiveIntegerField()
    description = models.TextField()  # Main recipe description
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set date
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updated on save
    slug = models.SlugField(unique=True, blank=True)  # URL-friendly identifier
    categories = models.ManyToManyField(
        Category,
        related_name='recipes',
        blank=True
    )  # Multiple categories per recipe

    # Cloudinary-hosted main image
    featured_image = CloudinaryField('image', default='placeholder')

    def save(self, *args, **kwargs):
        """Automatically generate slug from title and calculate total time"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        """Readable representation including title and author"""
        return f"{self.title} | written by {self.author}"


class Equipment(models.Model):
    """
    Represents kitchen equipment needed for a recipe.
    Each equipment item belongs to one recipe.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='equipment'  # Access via recipe.equipment.all()
    )
    name = models.CharField(max_length=100)  # Name of equipment item

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Represents an ingredient in a recipe, with optional quantity and notes.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'  # Access via recipe.ingredients.all()
    )
    quantity = models.CharField(max_length=50, blank=True)  # Optional qty
    name = models.CharField(max_length=100)  # Ingredient name
    notes = models.CharField(max_length=100, blank=True)  # Optional notes

    def __str__(self):
        """Combines quantity, name and notes (if available)"""
        return f"{self.quantity} {self.name} {self.notes}".strip()


class Instruction(models.Model):
    """
    Represents a step in the recipe instructions.
    Steps are ordered by step_number.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='instructions'  # Access via recipe.instructions.all()
    )
    step_number = models.PositiveIntegerField()  # Order of step
    content = models.TextField()  # Detailed instruction text

    class Meta:
        ordering = ['step_number']  # Ensure steps are always ordered correctly

    def __str__(self):
        return f"Step {self.step_number}"


class Comment(models.Model):
    """
    User comments on recipes, requiring approval before display.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments"  # Access via recipe.comments.all()
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="commenter"  # Access via user.commenter.all()
    )
    body = models.TextField()  # Comment text content
    approved = models.BooleanField(default=False)  # Moderation flag
    created_on = models.DateTimeField(auto_now_add=True)  # Comment timestamp

    class Meta:
        ordering = ["-created_on"]  # Show newest comments first

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
