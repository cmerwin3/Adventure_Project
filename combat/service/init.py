
from character.models import PC_Character, NPC_Character
from . import attack
from . import utility



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
        initiative = utility.dice_roll() + character["dexterity"]
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
        utility.save_game_state(position_list)
        results['turn_status'] = 'end_combat'
        end_combat_data = {}
        end_combat_data['conclusion'] = 'win'
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
        npc_turn_data, next_turn = attack.handle_npc_attack(position_list, turn_order_list, current_turn) 
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
    next_turn = utility.increment_turn(turn_order_list,current_turn)
    return is_dead, results, next_turn