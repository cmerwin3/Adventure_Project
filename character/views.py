'''
The Views for a Character
'''

from django.shortcuts import render
from django.http import Http404
from .models import PC_Character, NPC_Character
from django.http import JsonResponse
from django.forms.models import model_to_dict


def show_pc_character(request, character_id=None):
    try:
        if character_id is None:
            char = PC_Character.objects.first()
        else:
            char = PC_Character.objects.get(pk=character_id)
        #return render(request, 'character_sheet.html', {'character':char})
        #return JsonResponse(model_to_dict(char))
        return JsonResponse(char.to_dict(), json_dumps_params={'indent': 2})
    except PC_Character.DoesNotExist as exc:
        raise Http404("PC Character id ({}) not found.".format(character_id))


def show_npc_character(request, character_id=None):
    try:
        if character_id is None:
            char = NPC_Character.objects.first()
        else:
            char = NPC_Character.objects.get(pk=character_id)
        #return render(request, 'character_sheet.html', {'character':char})
        #return JsonResponse(model_to_dict(char))
        return JsonResponse(char.to_dict(), json_dumps_params={'indent': 2})
    except NPC_Character.DoesNotExist as exc:
        raise Http404("NPC Character id ({}) not found.".format(character_id))