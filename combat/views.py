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
    position_list, turn_order_list, background_image = service.init_combat(game_id)
    
    request.session['turn_order_list'] = turn_order_list
    request.session['position_list'] = position_list

    results = {}
    results['position_list'] = position_list
    results['turn_order_list'] = turn_order_list
    results['background'] = 'background-cavern.jpg'

    return JsonResponse(results, json_dumps_params={'indent': 2})

  




        





def do_combat(request):
    # url format: "/combat?action=attack&attacker_id=1&item_id=5&defender_id=9"
    action = request.GET.get('action', '')
    source_id = request.GET.get('source_id', '')
    item_id = request.GET.get('item_id', '')
    destination_id = request.GET.get('destination_id', '')

    if action == 'attack':
        service.attack(source_id, item_id, destination_id)
    else:
        raise Exception("Unknown action requested.")

    # After combat, redirect to main page
    return redirect('main-page')
