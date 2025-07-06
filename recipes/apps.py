from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """
    Application configuration class for the 'recipes' app.
    This configures application-specific settings and metadata.
    """

    # Specifies the default primary key field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # The name of the application
    name = 'recipes'
