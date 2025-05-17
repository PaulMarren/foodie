from django.contrib import admin
from .models import Recipe, Equipment, Ingredient, Instruction, Tip
from django_summernote.admin import SummernoteModelAdmin

class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 1

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1

class TipInline(admin.TabularInline):
    model = Tip
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [EquipmentInline, IngredientInline, InstructionInline, TipInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'total_time', 'created_at')