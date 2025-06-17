from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe, Equipment, Ingredient, Instruction, Comment


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['featured_image'].required = True
        self.fields['categories'].required = True

    class Meta:
        model = Recipe
        exclude = ['author', 'slug', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'prep_time': forms.NumberInput(attrs={'min': 0}),
            'cook_time': forms.NumberInput(attrs={'min': 0}),
            'total_time': forms.NumberInput(attrs={'min': 0}),
            'featured_image': forms.ClearableFileInput(attrs={'required': 'required'}),
            'categories': forms.CheckboxSelectMultiple(),  
        }

    def clean(self):
        cleaned_data = super().clean()
    
        categories = cleaned_data.get('categories')
        if not categories:
            self.add_error('categories', "Please select at least one category.")
    
        featured_image = cleaned_data.get('featured_image')
        if not featured_image:
            self.add_error('featured_image', "A featured image is required.")
    
        return cleaned_data



class EquipmentForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Blender, Mixing Bowl'}),
        required=True
    )

    class Meta:
        model = Equipment
        fields = ['name']


class IngredientForm(forms.ModelForm):
    quantity = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., 1 cup, 2 tbsp'}),
        required=False
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Flour, Sugar'}),
        required=True
    )
    notes = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Chopped, At room temperature'}),
        required=False
    )

    class Meta:
        model = Ingredient
        fields = ['quantity', 'name', 'notes']


class InstructionForm(forms.ModelForm):
    step_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1}),
        required=True
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe this step...'}),
        required=True
    )
    
    class Meta:
        model = Instruction
        fields = ['step_number', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

