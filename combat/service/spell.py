from . import utility
from ref_data.models import Spell, SpellType


def handle_pc_spell(destination_index, position_list, turn_order_list, current_turn, spell_id):
    spell = Spell.objects.get(pk = spell_id)
    if spell['spell_type'] == SpellType.ATTACK_SPELL:
        results, next_turn = cast_attack_spell(destination_index, position_list, turn_order_list, current_turn, spell)
    elif  spell['spell_type'] == SpellType.RESIST_SPELL:
        results, next_turn = cast_resist_spell(destination_index, position_list, turn_order_list, current_turn, spell)
    elif  spell['spell_type'] == SpellType.UTILITY_SPELL:
        results, next_turn = cast_utility_spell(destination_index, position_list, turn_order_list, current_turn, spell)

    return results, next_turn 

def cast_attack_spell(destination_index, position_list, turn_order_list, current_turn, spell):
    source = position_list[turn_order_list[current_turn]]
    destination = position_list[destination_index]
    
    natural, damage = attack_spell(source, destination, spell)
    
    results = {}
    if damage == 0:
        results['narration'] = f"The {source['name']} missed their spell against {destination['name']}."
    else:
        results['narration'] = f"The {source['name']} attacked {destination['name']} with a {spell['name']} for {damage} damage."
    results['destination_ids'] = [destination_index]
    results['damage'] = [damage]
    results['natural'] = [natural]
    next_turn = utility.increment_turn(turn_order_list,current_turn)

    return results, next_turn

def attack_spell(source, destination, spell):
    natural = utility.dice_roll()
    modifier = utility.get_modifier(source)
    result = modifier + natural + 2
    armor_class = destination['armor_class']
    if result >= armor_class:
        damage = utility.dice_roll(spell['damage_dice'])
        hit_points =  destination['hit_points_current'] - damage
        if hit_points < 0:
            hit_points = 0
        destination['hit_points_current'] = hit_points    
    else:
        damage = 0
    return natural, damage

def cast_resist_spell(destination_index, position_list, turn_order_list, current_turn, spell):
    source = position_list[turn_order_list[current_turn]]
    destination = position_list[destination_index]

    natural, damage = resist_spell(source, destination, spell)

    results = {}
    if damage == 0:
        results['narration'] = f"The {destination['name']} resisted the {spell['spell_name']} and only took {damage} damage."
    else:
        results['narration'] = f"The {source['name']} attacked {destination['name']} with a {spell['name']} for {damage} damage."
    results['destination_ids'] = [destination_index]
    results['damage'] = [damage]
    results['natural'] = [natural]
    next_turn = utility.increment_turn(turn_order_list,current_turn)

    return results, next_turn

def resist_spell(source, destination, spell):
    natural = utility.dice_roll()
    destination_modifier = utility.get_modifier(destination)
    source_modifier = utility.get_modifier(source)
    result = destination_modifier + natural 
    spell_difficulty = 10 + source_modifier
    damage = utility.dice_roll(spell['damage_dice'])
    if result >= spell_difficulty:
        hit_points =  destination['hit_points_current'] - damage/2
        if hit_points < 0:
            hit_points = 0
        destination['hit_points_current'] = hit_points
    else:
        hit_points =  destination['hit_points_current'] - damage
        if hit_points < 0:
            hit_points = 0
        destination['hit_points_current'] = hit_points    
    return natural, damage



def cast_utility_spell(destination_index, position_list, turn_order_list, current_turn, spell):
    return results



'''
def handle_pc_attack_spell(destination_index, position_list, turn_order_list, current_turn, spell):
    
    source = position_list[turn_order_list[current_turn]]
    destination = position_list[destination_index]
    
    natural, damage = attack_spell(source, destination, spell)
    
    results = {}
    if damage == 0:
        results['narration'] = f"The {source['name']} missed their attack against {destination['name']}."
    else:
        results['narration'] = f"The {source['name']} attacked {destination['name']} with a {spell['name']} for {damage} damage."
    results['destination_ids'] = [destination_index]
    results['damage'] = [damage]
    results['natural'] = [natural]
    next_turn = utility.increment_turn(turn_order_list,current_turn)

    return results, next_turn

'''

'''
def attack_spell(source, destination, spell):
    natural = utility.dice_roll()
    modifier = utility.get_modifier(source)
    result = modifier + natural + 2
    armor_class = destination['armor_class']
    if result >= armor_class:
        damage = utility.dice_roll(spell['damage_dice'])
        hit_points =  destination['hit_points_current'] - damage
        if hit_points < 0:
            hit_points = 0
        destination['hit_points_current'] = hit_points    
    else:
        damage = 0
    return natural, damage

'''