# Generated by Django 3.1.2 on 2021-11-12 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ref_data', '0009_auto_20210423_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='spell_type',
            field=models.CharField(choices=[('Attack_Spell', 'Attack Spell'), ('Resist_Spell', 'Resist Spell'), ('Utility_Spell', 'Utility Spell')], max_length=30, null=True),
        ),
    ]
