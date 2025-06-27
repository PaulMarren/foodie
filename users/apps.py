from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Application configuration class for the 'users' app.
    Configures application-specific settings and initialization.
    """
    
    # Specifies the default primary key field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    name = 'users'  # Name of the app

    def ready(self):
        """
        Method called when the app is fully loaded and ready.
        Used here to import and register signal handlers.
        """
        # Import signals module to connect signal handlers, signals are connected on import
        import users.signals