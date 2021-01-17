from django.db import models

# Create your models here.


class GameData(models.Model):

    user_name = models.CharField(max_length=30)
    
    password = models.CharField(max_length=30)
    
    last_script_id = models.CharField(max_length=20)

    completed_script_ids = models.CharField(max_length=500)



    class Meta:
         db_table = 'game_data'