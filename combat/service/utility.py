
from character import service as character_service
import random


def get_modifier(source, item):
    if item['has_finesse'] is True:
        modifier = max(source['strength'], source['dexterity'])
    else:
        modifier = source['strength']
    return modifier

def dice_roll(max_value=20):
    value = random.randint(1,max_value)
    return value

def increment_turn(turn_order_list,current_turn):
    current_turn += 1
    if current_turn == len(turn_order_list):
        current_turn = 0
    return current_turn

def save_game_state(position_list):
    index = 0
    while index < 4:
        character_sheet = position_list[index]
        id = character_sheet['id']
        hit_points_current = character_sheet['hit_points_current']
        character_service.update_pc_character_hit_points_current(id, hit_points_current)
        index += 1