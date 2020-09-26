import random
from django.db import models

# Create your models here.
def roll(max_value):
    value = random.randint(1,max_value)
    return value

prof = 2

cha = [3]

def attack():
    value = roll + prof + cha
    return value

dir()