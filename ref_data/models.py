from django.db import models

# Create your models here.

class Classes(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField()
    hit_dice = models.IntegerField()
    proficencies = models.CharField(max_length=30)
    #features 
    

'''
class Features_Clasess():   
    name 
    description
'''
    

class Races(models.Model):
    name = models.CharField(max_length=30)
    speed = models.IntegerField()
    hav_dv = models.BooleanField()
    #features
    str_bounus = models.IntegerField()
    dex_bonus = models.IntegerField()
    con_bonus = models.IntegerField()
    int_bonus = models.IntegerField()
    wis_bonus = models.IntegerField()
    cha_bonus = models.IntegerField()

'''class Features_Races():
    name
    description
'''
    
class Items(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    weight = models.IntegerField()
    damage_type = models.CharField(max_length=30)
    damage_dice = models.IntegerField()
    attack_modifier = models.IntegerField()


class Spells(models.Model):
    name = models.CharField(max_length=30)
    spell_level = models.IntegerField()
    school = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    damage_type = models.CharField(max_length=30)
    damage_dice = models.IntegerField()

