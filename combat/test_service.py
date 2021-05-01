import unittest
from unittest.mock import patch
from . import service
from character.models import PC_Character, NPC_Character

class test_combat(unittest.TestCase):
    
    test_character_dict = {'id' : 1, 'dexterity' : 0}

    test_PC_Character = PC_Character(id=1)

    test_NPC_Character = NPC_Character(id=2)

    test_pc_list = [test_PC_Character, test_PC_Character, test_PC_Character, test_PC_Character]

    items = [
        {'name': 'longsword', 'has_finesse': False, 'damage_dice': 8, 'attack_modifier': 0}
        ]

    position_list_none_dead = [
        {'id': 1, 'name': 'PC_1', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 2, 'name': 'PC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 3, 'name': 'PC_3', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 4, 'name': 'PC_4', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'name': 'NPC_1', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'name': 'NPC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items}
        ]

    position_list_all_pcs_dead = [
        {'id': 1, 'name': 'PC_1', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 2, 'name': 'PC_2', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 3, 'name': 'PC_3', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 4, 'name': 'PC_4', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'name': 'NPC_1', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'name': 'NPC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items}
        ]

    position_list_pc_dead = [
        {'id': 1, 'name': 'PC_1', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 2, 'name': 'PC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 3, 'name': 'PC_3', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'id': 4, 'name': 'PC_4', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'name': 'NPC_1', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items},
        {'name': 'NPC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'armor_class': 10, 'items': items}
        ]

    position_list_all_npcs_dead = [
        {'id': 1, 'name': 'PC_1', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'id': 2, 'name': 'PC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'id': 3, 'name': 'PC_3', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'id': 4, 'name': 'PC_4', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'name': 'NPC_1', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'name': 'NPC_2', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'items': items}
        ]

    position_list_npc_dead = [
        {'id': 1, 'name': 'PC_1', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'id': 2, 'name': 'PC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'id': 3, 'name': 'PC_3', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'id': 4, 'name': 'PC_4', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'name': 'NPC_1', 'hit_points_current': 0, 'hit_points_total': 10, 'strength' : 2, 'items': items},
        {'name': 'NPC_2', 'hit_points_current': 10, 'hit_points_total': 10, 'strength' : 2, 'items': items}
        ]

    test_npc_list = [ 'Goblin', 'Goblin'] 
    
    
    turn_order_list = [0,1,2,3,4,5]

    '''
    Test case for init_combat
    '''
    @patch('character.models.NPC_Character.objects')  
    @patch('character.models.PC_Character.objects') 
    @patch('character.models.Character.to_dict')
    def test_init_combat(self, mock_to_dict, mock_pc_character_objects, mock_npc_character_objects):
        mock_to_dict.return_value = self.test_character_dict
        mock_pc_character_objects.filter.return_value = self.test_pc_list
        mock_npc_character_objects.filter.return_value.first.return_value = self.test_NPC_Character
        position_list, turn_order_list = service.init_combat(1, self.test_npc_list)
        assert len(position_list) == 6
        assert len(turn_order_list) == 6
         

    '''
    Test case suite for death_check()
    '''    
    def test_death_check_none_dead(self):
        is_dead, results, current_turn = service.death_check(
            self.position_list_none_dead, self.turn_order_list, 0)
        assert is_dead == False
        assert len(results) == 0
        assert current_turn == 0
    
    def test_death_check_pc_dead(self):
        is_dead, results, next_turn = service.death_check(
            self.position_list_pc_dead, self.turn_order_list, 0)
        assert is_dead == True
        assert results['status'] == 'dead'
        assert next_turn == 1

    def test_death_check_npc_dead(self):
        is_dead, results, next_turn = service.death_check(
            self.position_list_npc_dead, self.turn_order_list, 4)
        assert is_dead == True
        assert results['status'] == 'dead'
        assert next_turn == 5

    '''
    Test case suite for team_death_check()
    '''        
    def test_team_death_check_none_dead(self):
        pc_any_alive, npc_any_alive = service.team_death_check(
            self.position_list_none_dead)
        assert pc_any_alive == True
        assert npc_any_alive == True

    def test_team_death_check_pcs_dead(self):
        pc_any_alive, npc_any_alive = service.team_death_check(
            self.position_list_all_pcs_dead)
        assert pc_any_alive == False
        assert npc_any_alive == True

    def test_team_death_check_npcs_dead(self):
        pc_any_alive, npc_any_alive = service.team_death_check(
            self.position_list_all_npcs_dead)
        assert pc_any_alive == True
        assert npc_any_alive == False

    '''
    Test case suite for init_turn()
    '''
    def test_init_turn_pcs_dead(self):
        results, next_turn = service.init_turn(
            self.position_list_all_pcs_dead, self.turn_order_list, 0)
        assert 'end_combat_data' in results
        end_combat_data = results['end_combat_data']
        assert end_combat_data['conclusion'] == 'loss'
        assert results['turn_status'] == 'end_combat'

    @patch('character.service.update_pc_character_hit_points_current')
    def test_init_turn_npcs_dead(self, mock_character_service):
        results, next_turn = service.init_turn(
            self.position_list_all_npcs_dead, self.turn_order_list, 0)
        assert 'end_combat_data' in results
        end_combat_data = results['end_combat_data']
        assert end_combat_data['conclusion'] == 'win'
        assert results['turn_status'] == 'end_combat'

    def test_init_turn_current_pc_is_dead(self):
        results, next_turn = service.init_turn(
            self.position_list_pc_dead, self.turn_order_list, 0)
        assert results['turn_status'] == 'skip_turn'

    def test_init_turn_current_npc_is_dead(self):
        results, next_turn = service.init_turn(
            self.position_list_npc_dead, self.turn_order_list, 4)
        assert results['turn_status'] == 'skip_turn'

    def test_init_turn_pc_turn(self):
        results, next_turn = service.init_turn(
            self.position_list_none_dead, self.turn_order_list, 0)
        assert results['turn_status'] == 'pc_turn'

    
    def test_init_turn_npc_turn(self):
        results, next_turn = service.init_turn(
            self.position_list_none_dead, self.turn_order_list, 4)
        assert results['turn_status'] == 'npc_turn'

