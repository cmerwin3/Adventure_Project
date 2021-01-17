from django.shortcuts import render
from django.http import HttpResponse

from ref_data.models import ClassLevel, Race, Item, Spell

#from ref_data import Item
from character.models import Character
#from dice.models import roll 
#import dice
from dice import models as dice


def attack(attacker_id, item_id, defender_id):
    # TODO change 'attacker' to 'source'
    attacker = Character.objects.get(pk = attacker_id)
    # TODO change 'defender' to 'destination'
    defender = Character.objects.get(pk = defender_id)
    item = Item.objects.get(pk = item_id)

    #natural = roll()
    natural = dice.roll()
    # TODO Natrual 1
    # TODO Natrual 20
    
    # TODO change 'attacker' to 'source'
    modifier = get_modifier(attacker,item)
    
    result = modifier + natural
    # TODO finesse
    
    # TODO change 'defender' to 'destination'
    armor_class = defender.armor_class

    # TODO change 'defender' to 'destination'
    if result >= armor_class:
        damage = get_damage(item.damage_dice, modifier)
        hit_points = get_hit_points(damage, defender.hit_points_current)
        save_hit_points(hit_points, defender)
    else:
        damage = None
    
    return natural, modifier, damage

def get_damage(item_damage_dice, modifier):
    damage = dice.roll(item_damage_dice) + modifier
    return damage

# TODO change 'defender' to 'destination'
def get_hit_points(damage, defender_hit_points_current):
    hit_points =  defender_hit_points_current - damage
    if hit_points < 0:
        hit_points = 0
    return hit_points

# TODO change 'defender' to 'destination'
def save_hit_points(hit_points, defender):
    #TODO  save currnet hitpoints to session not database
    defender.hit_points_current = hit_points
    defender.save()

# TODO change 'attacker' to 'source'
def get_modifier(attacker, item):
    if item.has_finesse is True:
        modifier = max(attacker.strength, attacker.dexterity)
    else:
        modifier = attacker.strength
    return modifier