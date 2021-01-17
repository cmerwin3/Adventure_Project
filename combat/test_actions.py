import unittest
from unittest.mock import patch
from combat import actions
import dice.models


class Test_Actions(unittest.TestCase):

    @patch('combat.actions.dice')
    def test_get_damage_roll_3(self, mock_dice):
        mock_dice.roll.return_value = 3
        
        # TODO change 'attacker' to 'source'
        result = actions.get_damage(item_damage_dice=8, attacker_strength=2)
        assert result == 5

    @patch('combat.actions.dice')
    def test_get_damage_roll_5(self, mock_dice):
        mock_dice.roll.return_value = 5

        # TODO change 'attacker' to 'source'
        result = actions.get_damage(item_damage_dice=8, attacker_strength=2)
        assert result == 7

    def test_get_hit_points(self):
        # TODO change 'defender' to 'destination'
        result = actions.get_hit_points(damage=10, defender_hit_points_current=20)
        assert result == 10

    def test_get_hit_points_negative_ints(self):
        # TODO change 'defender' to 'destination'
        result = actions.get_hit_points(damage=20, defender_hit_points_current=10)
        assert result == 0
