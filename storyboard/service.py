from character.models import PC_Character, NPC_Character

def get_script(request, game_id, script_id):
    background_image, npc_id_list = get_scene(script_id)
    
    data = {} 
    
    data['script_id'] = 'town.' 
    
    data['background_image'] = background_image
   
    data['position_list'] = generate_possition_list(game_id, npc_id_list)
    
    data['prompt'] = ('Walking into town you see a bustiling fair in progress.'
                    'The atmosphere is filled with jovial music and the aroma of baked goods.'
                    'A well dressed townsperson greets you with arms full of mugs of ale. "Welcome to Stratengrad, and happy new year!"')
    data['responses'] = [   {'response_id' : 'A', 
                            'response' : 'Accept the ale.'},
                            {'response_id' : 'B', 
                            'response' : 'Toast to thier health.'},
                            {'response_id' : 'C', 
                            'response' : 'Slap the ale from their hand.'},
                            {'response_id' : 'D', 
                            'response' : 'Walk away.'}
                        ]
    return data

def get_scene(script_id): #TODO Make dynamic relative to json
    npc_id_list = [1,1,2]
    
    return "background-mine.jpg", npc_id_list


def generate_possition_list(game_id, npc_id_list):
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

    return position_list








'''
Combat Funtions
'''
def init_combat(script_id):
    
    npc_id_list = [1,1,1]
    
    return "background-mine.jpg", npc_id_list
