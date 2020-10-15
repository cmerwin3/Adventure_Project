from django.db import models

class ClassType(models.TextChoices):
    CLERIC = 'Cleric'
    FIGHTER = 'Fighter'
    ROUGE = 'Rouge'
    WIZARD = 'Wizard'

class RaceType(models.TextChoices):
    DWARF = 'Dwarf'
    ELF = 'Elf'
    HALFLING = 'Halfling'
    HUMAN = 'Human'

class DamageType(models.TextChoices):
    BLUDGEONING = 'Bludgeoning'
    PIERCING = 'Piercing'
    SLASHING = 'Slashing'
    FORCE = 'Force'
    FIRE = 'Fire'
    FROST = 'Frost'
    LIGHTNING = 'Lightning'
    POISON = 'Poison'
    ACID = 'Acid'
    NECROTIC = 'Necrotic'
    RADIANT = 'Radiant'
    HEALING = 'Healing'

class SchoolType(models.TextChoices) :
    ABJURATION ='Abjuration'
    CONJURATION = 'Conjuration'
    DIVINATION = 'Divination'
    ENCHANTMENT = 'Enchantment'
    EVOCATION = 'Evocation'
    ILLUSION = 'Illusion'
    NECROMANCY = 'Necromancy'
    TRANSMUTATION = 'Transmutaion'


'''
class Ability(models.TextChoices):
    STRENGTH = 'Strength'
    DEXTERITY = 'Dexterity'
    CONSTITUTION = 'Constitution'
    INTELLEGENCE = 'Intellegence'
    WISDOM = 'Wisdom'
    CHARISMA = 'Charisma'

class Skill(models.TextChoices):
    ACROBATICS = 
    ANIMAL_HANDILING = 
'''

    
    

    
class ClassLevel(models.Model):
    class_type = models.CharField(max_length=30, null=True, choices=ClassType.choices)
    level = models.IntegerField()
    hit_dice_type = models.IntegerField()
    '''proficencies = models.CharField(max_length=30)
    proficencies_bounus= models.IntegerField()'''
    spell_slot = models.IntegerField()
    class Meta:
        db_table = 'class_level'

    
    

class Race(models.Model):
    race_type = models.CharField(max_length=30, null=True, choices=RaceType.choices)
    speed = models.IntegerField()
    hav_dv = models.BooleanField()
    str_bounus = models.IntegerField()
    dex_bonus = models.IntegerField()
    con_bonus = models.IntegerField()
    int_bonus = models.IntegerField()
    wis_bonus = models.IntegerField()
    cha_bonus = models.IntegerField()
    class Meta: 
        db_table = 'race'


    
class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    weight = models.IntegerField()
    damage_type = models.CharField(max_length=30, null=True, choices=DamageType.choices)
    damage_dice = models.IntegerField()
    attack_modifier = models.IntegerField()
    class Meta: 
        db_table = 'item'


class Spell(models.Model):
    name = models.CharField(max_length=30)
    spell_level = models.IntegerField()
    school = models.CharField(max_length=30, null=True, choices=SchoolType.choices)
    description = models.CharField(max_length=100)
    damage_type = models.CharField(max_length=30, null=True, choices=DamageType.choices)
    damage_dice = models.IntegerField()
    class Meta: 
        db_table = 'spell'

