from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    prep_time = models.PositiveIntegerField(help_text="Prep time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cook time in minutes")
    total_time = models.PositiveIntegerField(help_text="Total time in minutes")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    featured_image = CloudinaryField('image', default='placeholder')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | written by {self.author}" 

class Equipment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    section = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    quantity = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)
    notes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.name} {self.notes}".strip()

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveIntegerField()
    content = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}"

class Tip(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='tips')
    content = models.TextField()

    def __str__(self):
        return self.content[:50] + "..."