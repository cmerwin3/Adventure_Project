from django.shortcuts import render
from django.http import JsonResponse
from . import service


def get_script(request, script_id=None):
    game_id = request.session['game_id']
    data = service.get_script(request, game_id, script_id)
   
    return JsonResponse(data, json_dumps_params={'indent': 2})

def handle_response(request, script_id, response_id):
    game_id = request.session['game_id']
    data = service.handle_response(request, game_id, script_id, response_id)
   
    return JsonResponse(data, json_dumps_params={'indent': 2})