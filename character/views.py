'''
The Views for a Character
'''

from django.shortcuts import render
from django.http import Http404
from .models import Character
from django.http import JsonResponse
from django.forms.models import model_to_dict

def show_character(request, character_id=None):
    try:
        if character_id is None:
            char = Character.objects.first()
        else:
            char = Character.objects.get(pk=character_id)
        #return render(request, 'character_sheet.html', {'character':char})
        #return JsonResponse(model_to_dict(char))
        return JsonResponse(char.to_dict(), json_dumps_params={'indent': 2})
    except Character.DoesNotExist as exc:
        raise Http404("Character id ({}) not found.".format(character_id))
