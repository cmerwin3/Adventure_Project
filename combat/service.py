from django.shortcuts import render
from django.http import HttpResponse
from storyboard import service as storyboard_service
from character.models import PC_Character, NPC_Character
from ref_data.models import ClassLevel, Race, Item, Spell

#from ref_data import Item
from character.models import Character
#from dice.models import roll 
#import dice
from dice import models as dice

def init_combat(game_id):
    background_image, npc_id_list = storyboard_service.init_combat(1) #TODO storyboard service 
    player_character_list = PC_Character.objects.filter(game_id = game_id)
    print('PC_Character='+ str(player_character_list)) #shows results to console
    non_player_character_list = []
    for id in npc_id_list:
        non_player_character_list.append(NPC_Character.objects.get(pk = id))

    position_list = []
    #position 0-3 is always PC characters
    for character in player_character_list:
        position_list.append(character.to_dict())

    #position 4-x is always NPC characters
    for character in non_player_character_list:
        position_list.append(character.to_dict())
    
    turn_order_list = generate_turn_order(position_list)

    return position_list, turn_order_list, background_image



def generate_turn_order(position_list):
    #create a list of pairs containing position in UI and initiative roll
    initiative_list = []
    index = 0
    for character in position_list:
        initiative = dice.roll() + character["dexterity"]
        initiative_list.append({'position':index,'initiative':initiative})
        index += 1
    # Sort list by initiatve roll
    initiative_list.sort(key=sortfunc)
    # Create new list of positions in order of initiative
    turn_order_list = []
    for entry in initiative_list:
        turn_order_list.append(entry['position'])
    return turn_order_list

def sortfunc(entry):  
     return entry['initiative']



def attack(source_id, item_id, destination_id):
    
    source = Character.objects.get(pk = source_id)
    
    destination = Character.objects.get(pk = destination_id)
    item = Item.objects.get(pk = item_id)

    #natural = roll()
    natural = dice.roll()
    # TODO Natrual 1
    # TODO Natrual 20
    

    modifier = get_modifier(source,item)
    
    result = modifier + natural
    # TODO finesse
    
    
    armor_class = destination.armor_class

    
    if result >= armor_class:
        damage = get_damage(item.damage_dice, modifier)
        hit_points = get_hit_points(damage, destination.hit_points_current)
        save_hit_points(hit_points, destination)
    else:
        damage = None
    
    return natural, modifier, damage

def get_damage(item_damage_dice, modifier):
    damage = dice.roll(item_damage_dice) + modifier
    return damage


def get_hit_points(damage, destination_hit_points_current):
    hit_points =  destination_hit_points_current - damage
    if hit_points < 0:
        hit_points = 0
    return hit_points


def save_hit_points(hit_points, destination):
    #TODO  save currnet hitpoints to session not database
    destination.hit_points_current = hit_points
    destination.save()


def get_modifier(source, item):
    if item.has_finesse is True:
        modifier = max(source.strength, source.dexterity)
    else:
        modifier = source.strength
    return modifier