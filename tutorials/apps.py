from django.apps import AppConfig

class Meta:
        managed = False
        db_table = 'tutorials_mytutorial'
        
class TutorialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutorials'
