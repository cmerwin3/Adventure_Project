# Generated by Django 3.1.1 on 2021-01-03 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_data', '0002_auto_20201220_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedata',
            name='pin',
        ),
        migrations.AddField(
            model_name='gamedata',
            name='password',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]