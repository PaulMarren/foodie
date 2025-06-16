from django.urls import path 
from . import views 
from .views import RecipeCreateView

urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('category/<slug:category_slug>/', views.home, name='recipes_by_category'),
    path('recipe/<slug:slug>/comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('recipe/<slug:slug>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]