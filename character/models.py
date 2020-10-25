from django.db import models

from ref_data.models import ClassLevel, Race, Item, Spell

class Character(models.Model):
    
    name = models.CharField(max_length=30)

    is_pc = models.BooleanField()
    
    class_level = models.ForeignKey(ClassLevel, null=True, on_delete=models.SET_NULL)
    
    race = models.ForeignKey(Race, null=True, on_delete=models.SET_NULL)

    items = models.ManyToManyField(Item)

    spells = models.ManyToManyField(Spell)
    
    hit_dice_current = models.IntegerField()

    hit_points_total = models.IntegerField()
    hit_points_current = models.IntegerField()
    
    
    armor_class = models.IntegerField()
    
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    '''
    strength_save = models.BooleanField()
    dexterity_save = models.BooleanField()
    constitution_save = models.BooleanField()
    intellegence_save = models.BooleanField()
    wisdom_save = models.BooleanField()
    charisma_save = models.BooleanField()

    passive_insight = models.IntegerField()
    passive_investigation = models.IntegerField()
    passive_perception = models.IntegerField()
    '''

    class Meta:
        db_table = 'character'

