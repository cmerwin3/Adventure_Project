'''
The Views for a Character
'''
from django.shortcuts import render
import character


def home(request):
    char = Character.objects.first()
    return render(request, 'character_sheet.html', {'character':char})
