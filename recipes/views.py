from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from .models import (Recipe, Equipment,
                     Ingredient, Instruction, Category, Comment)
from .forms import (RecipeForm, EquipmentForm,
                    IngredientForm, InstructionForm, CommentForm)


def home(request, category_slug=None):
    """
    Homepage view displaying recipes, optionally filtered by category.
    Features pagination and category sidebar.
    """
    # Filter recipes by category if category_slug is provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        recipe_list = Recipe.objects.filter(
            categories=category).order_by('-created_at')
    else:
        category = None
        recipe_list = Recipe.objects.all().order_by('-created_at')

    paginator = Paginator(recipe_list, 6)  # Show 6 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_categories = Category.objects.all()  # Get all categories for nav

    context = {
        'recipe_list': page_obj,
        'current_category': category,
        'all_categories': all_categories,
        'is_paginated': page_obj.has_other_pages(),
        'title': f'{category.name} Recipes - foodie',
    }
    return render(request, 'recipes/index.html', context)


class RecipeList(generic.ListView):
    """
    Alternative list view for recipes using Django's generic ListView.
    Shows all recipes with pagination (6 per page).
    """
    queryset = Recipe.objects.all()
    template_name = "recipes/index.html"
    paginate_by = 6


def recipe_detail(request, slug):
    """
    Detailed view for a single recipe, including comments and comment form.
    Handles both displaying the recipe and processing new comments.
    """
    recipe = get_object_or_404(Recipe, slug=slug)  # Recipe or return 404
    # Get approved comments
    # + unapproved comments by the current user (if authenticated)
    comments = recipe.comments.filter(
        Q(approved=True) |
        Q(approved=False,
          author=request.user.id if request.user.is_authenticated
          else None)
    ).order_by("-created_on")

    # Handle comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create comment but don't save yet
            new_comment = comment_form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment is awaiting approval!')
            return redirect('recipe_detail', slug=slug)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "recipes/recipe_detail/recipe_detail.html",
        {
            "recipe": recipe,
            "comments": comments,
            "comment_form": comment_form,
            "title": f"{recipe.title} - foodie",
        },
    )


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating new recipes with nested formsets for equipment,
    ingredients, and instructions. Requires login.
    """
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form/recipe_form.html'

    def get_formset_classes(self):
        """
        Returns a dictionary of formset classes
        used in the recipe creation form.
        """
        return {
            'equipment_formset': inlineformset_factory(
                Recipe, Equipment,
                form=EquipmentForm,
                extra=0,
                can_delete=False,
                min_num=1,
                validate_min=True
            ),
            'ingredient_formset': inlineformset_factory(
                Recipe, Ingredient,
                form=IngredientForm,
                extra=0,
                can_delete=False,
                min_num=1,
                validate_min=True
            ),
            'instruction_formset': inlineformset_factory(
                Recipe, Instruction,
                form=InstructionForm,
                extra=0,
                can_delete=False,
                min_num=1,
                validate_min=True
            ),
        }

    def get_context_data(self, **kwargs):
        """
        Adds formsets to the template context
        and sets initial step numbers for instructions.
        """
        context = super().get_context_data(**kwargs)
        formsets = self.get_formset_classes()

        # Add each formset to context with appropriate prefix
        for name, formset in formsets.items():
            context[name] = formset(prefix=name.split('_')[0])

            # For instruction formset, set initial step numbers
            if name == 'instruction_formset':
                for i, form in enumerate(context[name]):
                    form.initial['step_number'] = i + 1

        return context

    def form_invalid(
            self, form,
            equipment_formset=None, ingredient_formset=None,
            instruction_formset=None):
        """
        Handles invalid form submissions,
        preserving formset data for correction.
        """
        context = self.get_context_data()
        context['form'] = form

        # Use provided formsets if available, otherwise create new ones
        formsets = self.get_formset_classes()
        context['equipment_formset'] = (
            equipment_formset or
            formsets['equipment_formset'](prefix='equipment')
        )
        context['ingredient_formset'] = (
            ingredient_formset or
            formsets['ingredient_formset'](prefix='ingredient')
        )
        context['instruction_formset'] = (
            instruction_formset or
            formsets['instruction_formset'](prefix='instruction')
        )

        return self.render_to_response(context)

    def form_valid(self, form):
        """
        Processes valid form submissions,
        saving the recipe and all related formsets.
        """
        form.instance.author = self.request.user
        formsets = self.get_formset_classes()

        # Initialize all formsets with POST data and instance
        equipment_formset = formsets['equipment_formset'](
            self.request.POST,
            instance=form.instance,
            prefix='equipment')
        ingredient_formset = formsets['ingredient_formset'](
            self.request.POST,
            instance=form.instance,
            prefix='ingredient')
        instruction_formset = formsets['instruction_formset'](
            self.request.POST,
            instance=form.instance,
            prefix='instruction')

        # Validate all formsets
        if (equipment_formset.is_valid()
            and ingredient_formset.is_valid()
                and instruction_formset.is_valid()):

            self.object = form.save()
            equipment_formset.save()
            ingredient_formset.save()
            instruction_formset.save()
            return super().form_valid(form)
        else:
            # If formsets are invalid, return form_invalid with the formsets
            return self.form_invalid(
                form,
                equipment_formset=equipment_formset,
                ingredient_formset=ingredient_formset,
                instruction_formset=instruction_formset
            )

    def get_success_url(self):
        # Redirect to the newly created recipe's detail page
        messages.success(self.request, 'Recipe created successfully!')
        return reverse_lazy('recipe_detail', kwargs={'slug': self.object.slug})


def comment_edit(request, slug, comment_id):
    """
    Handles editing of existing comments.
    Only allows edits by the original author.
    Resets approval status when edited.
    """
    if request.method == "POST":

        recipe = get_object_or_404(Recipe, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id, recipe=recipe)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.approved = False  # Reset approval status on edit
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating comment!')

    return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    Handles deletion of comments. Only allows deletion by the original author.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(
            request, messages.ERROR,
            'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))
