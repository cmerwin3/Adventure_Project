'''
This logic is called on when a user saves or loads game data.
'''

from .models import GameData


def save_last_script(script_id, game_id):
    game_data = GameData.objects.get(pk = game_id)
    game_data.last_script_id = script_id
    game_data.save()

def get_last_script(game_id):
    game_data = GameData.objects.get(pk = game_id)
    script_id = game_data.last_script_id

    return script_id