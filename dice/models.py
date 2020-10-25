import random
from django.db import models

# Create your models here.
def roll(max_value=20):
    value = random.randint(1,max_value)
    return value