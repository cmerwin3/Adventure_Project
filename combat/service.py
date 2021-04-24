'''
This logic handles the initiation, turn sequence, and exit of combat mode, including the actions of npc-characters. 
'''

from django.shortcuts import render
from django.http import HttpResponse
from storyboard import service as storyboard_service
from character.models import PC_Character, NPC_Character
from ref_data.models import ClassLevel, Race, Item, Spell
import random



def init_combat(game_id, npc_list):
    '''
    Called to gather the list of PCs and NPCs then compile them into the position_list to be used in combat.
    '''
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
    '''
    Randomly determins the order of turns in combat.
    '''
    initiative_list = []
    index = 0
    for character in position_list:
        initiative = dice_roll() + character["dexterity"]
        initiative_list.append({'position':index,'initiative':initiative})
        index += 1
    
    initiative_list.sort(key=sortfunc)
    
    turn_order_list = []
    for entry in initiative_list:
        turn_order_list.append(entry['position'])
    return turn_order_list

def sortfunc(entry):  
     return entry['initiative']


def init_turn(position_list, turn_order_list, current_turn):
    '''
    Called at the begining of each turn to determine one of five scenarios 
    
    1. If all PCs have zero hit points result in Game Over
    2. If all NPCs have zero hit points result in Victory
    3. If the current turn (PC or NPC) has zero hit points then skip the current turn
    4. Is a PCs turn (if so wait for user input)
    5. Is a NPCs turn (if so make an automated attack)
    '''
    results = {}
    results['current_turn'] = current_turn

    pc_party_alive, npc_party_alive = team_death_check(position_list)
    is_dead, skip_turn_data, next_turn = death_check(position_list, turn_order_list, current_turn)
    
    if not pc_party_alive:
        results['turn_status'] = 'end_combat'
        end_combat_data = {}
        end_combat_data['conclusion'] = 'loss'
        end_combat_data['narration'] = 'Game Over'
        end_combat_data['next_script'] = 'mines.intro'
        results['end_combat_data'] = end_combat_data

    elif not npc_party_alive:
        save_game_state(position_list)
        results['turn_status'] = 'end_combat'
        end_combat_data = {}
        end_combat_data['conclusion'] = 'win '
        end_combat_data['narration'] = 'You live to fight another day.'
        end_combat_data['next_script'] = 'town'
        results['end_combat_data'] = end_combat_data
    
    elif is_dead is True:
        results['turn_status'] = 'skip_turn'
        results['skip_turn_data'] = skip_turn_data
    
    elif turn_order_list[current_turn] <= 3:     
        
        results['turn_status'] = 'pc_turn'
        next_turn = current_turn
    else:  
        npc_turn_data, next_turn = handle_npc_attack(position_list, turn_order_list, current_turn) 
        results['turn_status'] = 'npc_turn'
        results['npc_turn_data'] = npc_turn_data
        
    return results, next_turn


def team_death_check(position_list): 
    '''
    Called to determin if any PCs or NPCs have 1 or more hit points and return each team as seperate variable
    '''
    pc_any_alive = False 
    npc_any_alive = False 

    for index in range(0,4):
        character = position_list[index]
        if character['hit_points_current'] > 0:
            pc_any_alive = True 
    
    for index in range(4,len(position_list)):
        character = position_list[index]
        if character['hit_points_current'] > 0:
            npc_any_alive = True
    
    return pc_any_alive, npc_any_alive


 
def death_check(position_list, turn_order_list, current_turn):
    is_dead = False
    source = position_list[turn_order_list[current_turn]]
    if source['hit_points_current'] > 0:
        return is_dead, {}, current_turn
    is_dead = True  
    results = {}
    results['status'] = 'dead'
    results['narration'] = f"The {source['name']} is unmoving on the ground."
    next_turn = increment_turn(turn_order_list,current_turn)
    return is_dead, results, next_turn

def handle_pc_attack(destination_index, position_list, turn_order_list, current_turn):
    '''
    Called when a user clicks the attack button and choses a target
    '''
    source = position_list[turn_order_list[current_turn]]
    destination = position_list[destination_index]
   
    item = source['items'][0]
    natural, damage = attack(source, item, destination)
    
    results = {}
    if damage == 0:
        results['narration'] = f"The {source['name']} missed their attack against {destination['name']}."
    else:
        results['narration'] = f"The {source['name']} attacked {destination['name']} with a {item['name']} for {damage} damage."
    results['destination_ids'] = [destination_index]
    results['damage'] = [damage]
    results['natural'] = [natural]
    next_turn = increment_turn(turn_order_list,current_turn)

    return results, next_turn


def handle_npc_attack(position_list, turn_order_list, current_turn):
    '''
    Called during an NPCs turn to randomly choose a PC to attack
    '''
    source = position_list[turn_order_list[current_turn]]
    
    while True:
        destination_index = dice_roll(4) - 1
        destination = position_list[destination_index]
        if int(destination['hit_points_current']) > 0:
            break  
    
    item = source['items'][0]
    natural, damage = attack(source, item, destination)
    
    results = {}
    if damage == 0:
        results['narration'] = f"The {source['name']} missed their attack against {destination['name']}."
    else:
        results['narration'] = f"The {source['name']} attacked {destination['name']} with a {item['name']} for {damage} damage."
    results['source_id'] = [turn_order_list[current_turn]]
    results['destination_ids'] = [destination_index]
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
    natural = dice_roll()
    modifier = get_modifier(source,item)
    result = modifier + natural + 2
    armor_class = destination['armor_class']
    if result >= armor_class:
        damage = dice_roll(item['damage_dice'])+ modifier
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

def save_game_state(position_list):
    index = 0
    while index < 4:
        character_dict = position_list[index] 
        id = character_dict["id"]
        character_sheet = PC_Character.objects.get(pk = id)
        character_sheet.hit_points_current = character_dict["hit_points_current"]
        character_sheet.save()
        index += 1


def dice_roll(max_value=20):
    value = random.randint(1,max_value)
    return value