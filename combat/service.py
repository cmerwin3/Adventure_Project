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

def init_combat(game_id, npc_list):
    player_character_list = PC_Character.objects.filter(game_id = game_id)
    non_player_character_list = []
    for name in npc_list:
        non_player_character_list.append(NPC_Character.objects.filter(name = name).first())

    position_list = []
    #position 0-3 is always PC characters
    for character in player_character_list:
        position_list.append(character.to_dict())

    #position 4-x is always NPC characters
    for character in non_player_character_list:
        position_list.append(character.to_dict())
    
    turn_order_list = generate_turn_order(position_list)

    return position_list, turn_order_list



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


def init_turn(position_list, turn_order_list, current_turn):
    if turn_order_list[current_turn] <= 3 : 
        results = {}
        results['is_pc'] = True
        results['current_turn'] = current_turn 
        next_turn = current_turn
    else:
        results, next_turn = handle_npc_attack(position_list, turn_order_list, current_turn)
        results['is_pc'] = False
        results['current_turn'] = current_turn 
       
    return results, next_turn


def handle_pc_attack(destination_index, position_list, turn_order_list, current_turn):
    source = position_list[turn_order_list[current_turn]]
    destination = position_list[destination_index]
   
    item = source['items'][0]
    natural, damage = attack(source, item, destination)
    
    results = {}
    if damage == 0:
        results['narration'] = f"The {source['name']} missed their attack against {destination['name']}."
    else:
        results['narration'] = f"The {source['name']} attacked {destination['name']} with a {item['name']} for {damage} damage."
    results['recipient_ids'] = [destination_index]
    results['damage'] = [damage]
    results['natural'] = [natural]
    next_turn = increment_turn(turn_order_list,current_turn)

    return results, next_turn


def handle_npc_attack(position_list, turn_order_list, current_turn):
    source = position_list[turn_order_list[current_turn]]
    destination_index = dice.roll(4) - 1
    destination = position_list[destination_index]
    item = source['items'][0]
    natural, damage = attack(source, item, destination)
    
    results = {}
    if damage == 0:
        results['narration'] = f"The {source['name']} missed their attack against {destination['name']}."
    else:
        results['narration'] = f"The {source['name']} attacked {destination['name']} with a {item['name']} for {damage} damage."
    results['recipient_ids'] = [destination_index]
    results['damage'] = [damage]
    results['natural'] = [natural]
    next_turn = increment_turn(turn_order_list,current_turn)

    return results, next_turn


    
def increment_turn(turn_order_list,current_turn):
    current_turn += 1
    if current_turn == len(turn_order_list):
        current_turn = 0
    return current_turn
          
        


def attack(source, item, destination):
    #Roll D20
    natural = dice.roll()
    # TODO Natrual 1
    # TODO Natrual 20
    
    #Str or Dex
    modifier = get_modifier(source,item)
    
    #Total to hit
    result = modifier + natural
    
    armor_class = destination['armor_class']

    
    if result >= armor_class:
        damage = dice.roll(item['damage_dice'])+ modifier
        hit_points =  destination['hit_points_current'] - damage
        if hit_points < 0:
            hit_points = 0
        destination['hit_points_current'] = hit_points    
    else:
        damage = 0
    
    return natural, damage

def get_modifier(source, item):
    if item['has_finesse'] is True:
        modifier = max(source['strength'], source['dexterity'])
    else:
        modifier = source['strength']
    return modifier
    