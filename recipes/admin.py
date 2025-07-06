from django.contrib import admin
from .models import (
    Recipe, Category, Equipment,
    Ingredient, Instruction, Comment)


# Inline admin classes for models that will be edited within the Recipe admin
class EquipmentInline(admin.TabularInline):
    """Allows editing Equipment models inline within the Recipe admin"""
    model = Equipment  # Specifies the model to use
    extra = 1  # Number of empty forms to display for adding new Equipment


class IngredientInline(admin.TabularInline):
    """Allows editing Ingredient models inline within the Recipe admin"""
    model = Ingredient
    extra = 1


class InstructionInline(admin.TabularInline):
    """Allows editing Instruction models inline within the Recipe admin"""
    model = Instruction
    extra = 1


# Category admin configuration
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Category model"""
    # Automatically generates slug from name when creating/editing
    prepopulated_fields = {'slug': ('name',)}

    # Fields to display in the list view
    list_display = ('name', 'slug', 'description')

    # Fields to enable searching in the admin
    search_fields = ('name', 'description')


# Recipe admin configuration
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Recipe model"""
    # Include inline editors for related models
    inlines = [EquipmentInline, IngredientInline, InstructionInline]

    # Automatically generates slug from title
    prepopulated_fields = {'slug': ('title',)}

    # Fields to display in the list view
    list_display = ('title', 'author', 'total_time', 'created_at',
                    'display_categories')

    # Allows multiple category selection with a filter interface
    filter_horizontal = ('categories',)

    def display_categories(self, obj):
        """Display all categories for a recipe as a comma-separated string"""
        return ", ".join([category.name for category in obj.categories.all()])

    # Sets the column header name in the admin list view
    display_categories.short_description = 'Categories'


# Basic registration for Comment model (using default admin options)
admin.site.register(Comment)
