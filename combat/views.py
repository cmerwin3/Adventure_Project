'''
The Views for Combat action
'''
from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import actions
from character.models import PC_Character, NPC_Character
from dice import models as dice 
#from storyboard. import 'script'
# from 'session'.'game_session' import game.id

def init_combat(request): 
    game_id = request.session['game_id']
    print('game_id='+ str(game_id))
    player_character_list = PC_Character.objects.filter(game_id = game_id)
    print('PC_Character='+ str(player_character_list))
    non_player_character_list = []
    non_player_character_list.append(NPC_Character.objects.get(pk = 1))

    position_list = []
    #position 0-3 is always PC characters
    for character in player_character_list:
        position_list.append(character.to_dict())

    #position 4-x is always NPC characters
    for character in non_player_character_list:
        position_list.append(character.to_dict())
    
    turn_order_list = generate_turn_order(position_list)
    
    request.session['turn_order_list'] = turn_order_list
    request.session['position_list'] = position_list

    results = {}
    results['background'] = 'background-cavern.jpg'
    results['turn_order_list'] = turn_order_list

    return JsonResponse(results, json_dumps_params={'indent': 2})

  
def sortfunc(entry):  
     return entry['initiative']

def generate_turn_order(position_list):
    #create a list of pairs containing position in UI and initiative roll
    initiative_list = []
    index = 0
    for character in position_list:
        initiative = dice.roll() + character["dexterity"]
        initiative_list.append({'position':index,'initiative':initiative})
        index += 1
    # Sort list by initiatve roll
    initiative_list.sort(key=sortfunc)
    # Create new list of positions in order of initiative
    turn_order_list = []
    for entry in initiative_list:
        turn_order_list.append(entry['position'])
    return turn_order_list

        




# TODO change 'attacker' to 'source'
def do_combat(request):
    # url format: "/combat?action=attack&attacker_id=1&item_id=5&defender_id=9"
    action = request.GET.get('action', '')
    attacker_id = request.GET.get('attacker_id', '')
    item_id = request.GET.get('item_id', '')
    defender_id = request.GET.get('defender_id', '')

    if action == 'attack':
        actions.attack(attacker_id, item_id, defender_id)
    else:
        raise Exception("Unknown action requested.")

    # After combat, redirect to main page
    return redirect('main-page')
