from django.contrib import admin
from .models import Recipe, Category, Equipment, Ingredient, Instruction, Comment


class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 1


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')    


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [EquipmentInline, IngredientInline, InstructionInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'total_time', 'created_at', 
                    'display_categories')

    filter_horizontal = ('categories',)

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    
    display_categories.short_description = 'Categories'


admin.site.register(Comment)