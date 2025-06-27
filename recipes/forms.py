from django import forms
from .models import Recipe, Equipment, Ingredient, Instruction, Comment


class RecipeForm(forms.ModelForm):
    """Form for creating and updating Recipe instances."""
    
    def __init__(self, *args, **kwargs):
        """Initialize form with custom field attributes and requirements."""
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['title'].required = True
        self.fields['description'].required = True
        # Make total_time read-only as it's calculated automatically
        self.fields['total_time'].widget.attrs['readonly'] = True
        self.fields['featured_image'].required = True
        self.fields['categories'].required = True

    class Meta:
        """Metadata options for the form."""
        model = Recipe
        # Exclude these fields from the form (handled elsewhere)
        exclude = ['author', 'slug', 'created_at', 'updated_at']
        widgets = {
            # Custom widgets for better UX
            'description': forms.Textarea(attrs={'rows': 3}),
            # Ensure time fields can't be negative
            'prep_time': forms.NumberInput(attrs={'min': 0}),
            'cook_time': forms.NumberInput(attrs={'min': 0}),
            'total_time': forms.NumberInput(attrs={'min': 0}),
            # Make file input for recipe image clearly required
            'featured_image': forms.ClearableFileInput(attrs={'required': 'required'}),
            # Display categories as checkboxes for multiple selection
            'categories': forms.CheckboxSelectMultiple(),  
        }

    def clean(self):
        """Custom form validation and data processing."""
        cleaned_data = super().clean()

        # Calculate total time from prep and cook times
        prep_time = cleaned_data.get('prep_time', 0)
        cook_time = cleaned_data.get('cook_time', 0)
        cleaned_data['total_time'] = prep_time + cook_time
    
        # Validate at least one category is selected
        categories = cleaned_data.get('categories')
        if not categories:
            self.add_error('categories', "Please select at least one category.")
    
        # Validate featured image is provided
        featured_image = cleaned_data.get('featured_image')
        if not featured_image:
            self.add_error('featured_image', "A featured image is required.")
    
        return cleaned_data


class EquipmentForm(forms.ModelForm):
    """Form for handling Equipment instances with placeholder text."""
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Blender, Mixing Bowl'}),
        required=True
    )

    class Meta:
        """Simple form configuration for Equipment model."""
        model = Equipment
        fields = ['name']  # Only show the name field


class IngredientForm(forms.ModelForm):
    """Form for handling Ingredient instances with custom placeholders."""
    quantity = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., 1 cup, 2 tbsp'}),
        required=False  # Quantity can be optional
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Flour, Sugar'}),
        required=True
    )
    notes = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'E.g., Chopped, At room temperature'}),
        required=False  # Notes are optional
    )

    class Meta:
        """Metadata for Ingredient form fields."""
        model = Ingredient
        fields = ['quantity', 'name', 'notes']  # Field display order


class InstructionForm(forms.ModelForm):
    """Form for handling cooking instructions with validation."""
    step_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1}),  # Steps start at 1
        required=True
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2, 
            'placeholder': 'Describe this step...'
        }),
        required=True
    )
    
    class Meta:
        """Simple form configuration for Instruction model."""
        model = Instruction
        fields = ['step_number', 'content']


class CommentForm(forms.ModelForm):
    """Simple form for user comments on recipes."""
    class Meta:
        model = Comment
        fields = ('body',)  # Only show the comment body field