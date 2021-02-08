from django.shortcuts import render, redirect
from django.http import HttpResponse
from game_data.models import GameData
from character.models import PC_Character

def home(request):
    game_id = request.session.get('game_id')
    user_name = request.session.get('user_name')
    if game_id is None : 
        # missing game_id means user has not logged in yet
        return render(request, 'login.html')

    data_dict = {} 
    return render(request, 'home.html', data_dict)

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        game = GameData.objects.filter(user_name = user_name).first()

        if game is None:
            error = 'Player Name not found.'
            return render(request, 'login.html' , {'error_message': error})
        if password != game.password:
            error = 'Invalid username or password.'
            return render(request, 'login.html' , {'error_message': error})

        request.session['game_id'] = game.id
        request.session['user_name'] = game.user_name
        return redirect('/')
    else:
        # '/login' url must have been called (as GET), so just display the page
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        game = GameData.objects.filter(user_name = user_name).first()
        if game is not None:
            error = 'Player Name is taken.'
            return render(request, 'register.html' , {'error_message': error})

        # create new GameData record and add PC party characters
        game = GameData()
        game.user_name = user_name
        game.password = password 
        game.save()
        generate_party(game)

        request.session['game_id'] = game.id
        request.session['user_name'] = game.user_name
        return redirect('/')
    else:
        # '/register' url must have been called (as GET), so just display the page
        return render(request, 'register.html')


def logout(request):
    if request.session['game_id'] is not None:
        del request.session['game_id']
    if request.session['user_name'] is not None:
        del request.session['user_name']
    return render(request, 'login.html')


'''
Upon regestration creates new character data based on original templates (Character.id 1-4) to begin new game.
'''
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
