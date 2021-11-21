from . import utility



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
    next_turn = utility.increment_turn(turn_order_list,current_turn)

    return results, next_turn


def handle_npc_attack(position_list, turn_order_list, current_turn):
    '''
    Called during an NPCs turn to randomly choose a PC to attack
    '''
    source = position_list[turn_order_list[current_turn]]
    
    while True:
        destination_index = utility.dice_roll(4) - 1
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
    next_turn = utility.increment_turn(turn_order_list,current_turn)

    return results, next_turn

def attack(source, item, destination):
    natural = utility.dice_roll()
    modifier = utility.get_modifier(source,item)
    result = modifier + natural + 2
    armor_class = destination['armor_class']
    if result >= armor_class:
        damage = utility.dice_roll(item['damage_dice'])+ modifier
        hit_points =  destination['hit_points_current'] - damage
        if hit_points < 0:
            hit_points = 0
        destination['hit_points_current'] = hit_points    
    else:
        damage = 0
    return natural, damage