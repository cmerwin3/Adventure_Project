'''
The Views for Combat action
'''
from django.shortcuts import render, redirect
from . import actions

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
