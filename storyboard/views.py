'''
Views for Script Mode
'''
from django.shortcuts import render
from django.http import JsonResponse
from . import service


def get_script(request, script_id=None):
    '''
    REST API used to gather the next script based on players choice of a response from the current script.
    '''
    game_id = request.session['game_id']
    data = service.get_script(request, game_id, script_id)
   
    return JsonResponse(data, json_dumps_params={'indent': 2})


def handle_response(request, script_id, response_id):
    game_id = request.session['game_id']
    data = service.handle_response(request, game_id, script_id, response_id)
    if "combat_mode" in data:
        next_script = data["next_script"]
        request.session['next_script'] = next_script
        request.session['combat_mode'] = data['combat_mode']


    return JsonResponse(data, json_dumps_params={'indent': 2})

