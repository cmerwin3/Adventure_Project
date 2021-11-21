'''
The Views for Combat Mode
'''

from django.http import JsonResponse
from .service import attack, init, spell






def init_combat(request): 
    '''
    REST API called by UI when transitioning from Script Mode into Combat Mode
    
    Parameters : Request from session for extraction of session data 
    Returns : A Json response of a dict composed of the characters involved in combat (position_list), 
            the order of turns in combat (turn_order_list), and the background to be displayed
    '''
    game_id = request.session['game_id']
    combat_mode = request.session['combat_mode'] 
    position_list, turn_order_list = init.init_combat(game_id, combat_mode['npc_list'])
    
    request.session['position_list'] = position_list
    request.session['turn_order_list'] = turn_order_list
    request.session['current_turn'] = 0

    results = {}
    results['position_list'] = position_list
    results['turn_order_list'] = turn_order_list
    results['background'] = combat_mode['background']

    return JsonResponse(results, json_dumps_params={'indent': 2})

def init_turn(request):
    '''
    REST API Called by UI during Combat Mode at the start of each turn in combat
    
    Parameters : Request from session for extraction of session data 
    Returns : A Json response of a dict composed of the results from init_turn in the combat.service
    '''
    position_list = request.session['position_list']
    turn_order_list = request.session['turn_order_list']
    current_turn = request.session['current_turn']
    results, next_turn = init.init_turn(position_list, turn_order_list, current_turn)
    
    request.session['current_turn'] = next_turn
    return JsonResponse(results, json_dumps_params={'indent': 2})


def get_positions(request):
    '''
    REST API called to refresh the current state of the position list and the character objects within
    '''
    position_list = request.session['position_list']
    results = {}
    results['position_list'] = position_list
    return JsonResponse(results, json_dumps_params={'indent': 2})


def do_attack(request):
    '''
    REST API called when the user intiates an attack in combat
    '''
    destination_index = int(request.GET.get('destination_index'))
    position_list = request.session['position_list']
    turn_order_list = request.session['turn_order_list']
    current_turn = request.session['current_turn']
    results, next_turn = attack.handle_pc_attack(destination_index, position_list, turn_order_list, current_turn)
    
    request.session['current_turn'] = next_turn
    return JsonResponse(results, json_dumps_params={'indent': 2})
    

def cast_spell(request):
    '''
    REST API called when a user initiates a spell in combat
    '''
    destination_index = int(request.GET.get('destination_index'))
    spell_id = int(request.GET.get('spell_id'))
    position_list = request.session['position_list']
    turn_order_list = request.session['turn_order_list']
    current_turn = request.session['current_turn']
    results, next_turn = spell.handle_pc_spell(destination_index, position_list, turn_order_list, current_turn, spell_id)
    
    request.session['current_turn'] = next_turn
    return JsonResponse(results, json_dumps_params={'indent': 2})