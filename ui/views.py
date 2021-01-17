from django.shortcuts import render
from django.http import HttpResponse
from game_data.models import GameData
from character.models import PC_Character

def home(request):
    game_id = request.session.get('game_id')
    if game_id is None : 
        return render(request, 'login.html')
    ## TODO ##
    return render(request, 'home.html', {'name':'Cameron'})

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        game = GameData.objects.get(user_name = user_name)
        if game is None:
            error = 'Player Name not found.'
            return render(request, 'login.html' , {'error_message': error})
        if password == game.password: 
            game_id = game.id 
            request.session['game_id'] = game_id
            return render(request, 'home.html')
        else: 
            error = 'Invalid username or password.'
            return render(request, 'login.html' , {'error_message': error})
    else:
        error = 'Form input expected.'
        return render(request, 'login.html' , {'error_message': error})


def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        game = GameData.objects.filter(user_name = user_name).first()
        if game is not None:
            error = 'Player Name is taken.'
            return render(request, 'register.html' , {'error_message': error})
        game = GameData()
        game.user_name = user_name
        game.password = password 
        game.save()
        request.session['game_id'] = game.id
        generate_party(game)
        return render(request, 'home.html')
    
    return render(request, 'register.html')

#Upon regestration creates new character data based on original templates (Character.id 1-4) to begin new game.
def generate_party(game):
    generate_party_member(game, 1)
    generate_party_member(game, 2)
    generate_party_member(game, 3)
    generate_party_member(game, 4)

def generate_party_member(game, pk):
    pc = PC_Character.objects.get(pk=pk)
    
    pc.id = None 
    
    pc.game = game
    
    pc.save()
  