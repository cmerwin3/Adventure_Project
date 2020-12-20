from django.db import models
from django.forms.models import model_to_dict
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

    '''
    Convert a Character instance to a dict (usefull for REST API's).  
    The standard model_to_dict() does not handle foreign key tables very well.
    '''
    def to_dict(self):
        data = {}                           # create empty dict
        opts = self._meta                   # get the metadata options for this class

        # add each field value to the dict (including foreign-key sub classes, not just id's)
        for field in opts.concrete_fields:  
            value = field.value_from_object(self)
            if field.name is 'class_level':
                if value is None:
                    data[field.name] = None
                else:
                    class_level = ClassLevel.objects.get(pk=value)
                    data[field.name] = model_to_dict(class_level)
            elif field.name is 'race':
                if value is None:
                    data[field.name] = None
                else:
                    race = Race.objects.get(pk=value)
                    data[field.name] = model_to_dict(race)
            else:
                data[field.name] = value

        # add each item and spell detailed instance to the dict
        for field in opts.many_to_many:
            object_list = []
            for obj in field.value_from_object(self):
                object_list.append(model_to_dict(obj))
            data[field.name] = object_list
        return data
