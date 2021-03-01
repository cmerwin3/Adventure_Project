'''
The Views for Combat action
'''
from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import service
from character.models import PC_Character, NPC_Character
from dice import models as dice 
#from storyboard. import 'script'
# from 'session'.'game_session' import game.id

def init_combat(request): 
    game_id = request.session['game_id']
    print('game_id='+ str(game_id))
    combat_mode = request.session['combat_mode'] 
    position_list, turn_order_list = service.init_combat(game_id, combat_mode['npc_list'])
    
    request.session['position_list'] = position_list
    request.session['turn_order_list'] = turn_order_list
    request.session['current_turn'] = 0


    results = {}
    results['position_list'] = position_list
    results['turn_order_list'] = turn_order_list
    results['background'] = combat_mode['background']

    return JsonResponse(results, json_dumps_params={'indent': 2})

def init_turn(request):
    position_list = request.session['position_list']
    turn_order_list = request.session['turn_order_list']
    current_turn = request.session['current_turn']
    results, current_turn = service.init_turn(position_list, turn_order_list, current_turn)
    
    request.session['current_turn'] = current_turn
    return JsonResponse(results, json_dumps_params={'indent': 2})


def get_positions(request):
    position_list = request.session['position_list']
    results = {}
    results['position_list'] = position_list
    return JsonResponse(results, json_dumps_params={'indent': 2})


def do_attack(request):
    destination_index = int(request.GET.get('destination_index'))
    position_list = request.session['position_list']
    turn_order_list = request.session['turn_order_list']
    current_turn = request.session['current_turn']
    results, current_turn = service.handle_pc_attack(destination_index, position_list, turn_order_list, current_turn)
    
    request.session['current_turn'] = current_turn
    return JsonResponse(results, json_dumps_params={'indent': 2})
    

