from django.shortcuts import render
from django.http import JsonResponse


def get_script(request,script_id):
    data = {} 
    #TODO Logic to determin next script id
    data['id'] = '1'
    data['prompt'] = ('Walking into town you see a bustiling fair in progress.'
                    'The atmosphere is filled with jovial music and the aroma of baked goods.'
                    'A well dressed townsperson greets you with arms full of mugs of ale. "Welcome to Stratengrad, and happy new year!"')
    data['responses'] = [   {'response_id' : 1, 
                            'response' : 'Accept the ale.'},
                            {'response_id' : 2, 
                            'response' : 'Toast to thier health.'},
                            {'response_id' : 3, 
                            'response' : 'Slap the ale from their hand.'},
                            {'response_id' : 4, 
                            'response' : 'Walk away.'}
                        ]
    return JsonResponse(data, json_dumps_params={'indent': 2})