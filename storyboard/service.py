'''
Logic for the storyboard and the handling of individual scripts.
'''


from character.models import PC_Character, NPC_Character
from . import models
from game_data import service as game_data_service


def get_script(request, game_id, script_id):
    if not script_id:
        script_id = game_data_service.get_last_script(game_id)
        if not script_id:
            script_id = "town.intro"
    script = models.get_script(script_id)
    script['position_list'] = generate_position_list(game_id, script)
    
    game_data_service.save_last_script(script_id, game_id)

    return script

def generate_position_list(game_id, script):
    player_character_list = PC_Character.objects.filter(game_id = game_id)
    non_player_character_list = []
    for name in script['npc_list']:
        non_player_character_list.append(NPC_Character.objects.filter(name = name).first())
    
    
    position_list = []
    #position 0-3 is always PC characters
    for character in player_character_list:
        position_list.append(character.to_dict())

    #position 4-x is always NPC characters
    for character in non_player_character_list:
        position_list.append(character.to_dict())

    return position_list

def handle_response(request, game_id, script_id, response_id):
    script = models.get_script(script_id)
    response_list = script['responses']
    response = response_list[int(response_id)]
    
    data = {} 
    if 'combat_mode' in response: 
        combat_mode = response['combat_mode']
        if len(combat_mode['npc_list']) == 0:
            combat_mode['npc_list'] = script['npc_list']
        if len(combat_mode['background']) == 0:
            combat_mode['background'] = script['background']
        data['combat_mode'] = response['combat_mode']
    data['next_script'] = response['next_script']

    return data
   

def init_combat(script_id):
    
    npc_id_list = [1,1,1]
    
    return "background-mine.jpg", npc_id_list
