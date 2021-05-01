'''
Service layer for Character models
'''

from .models import PC_Character


def update_pc_character_hit_points_current(id, hit_points_current):
    character_sheet = PC_Character.objects.get(pk = id)
    if hit_points_current > character_sheet.hit_points_total:
        hit_points_current = character_sheet.hit_points_total
    if hit_points_current < 0:
        hit_points_current = 0
    character_sheet.hit_points_current = hit_points_current
    character_sheet.save()

