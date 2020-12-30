# Generated by Django 3.1.1 on 2020-09-26 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ref_data', '0004_auto_20200926_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='name',
        ),
        migrations.AddField(
            model_name='race',
            name='race_type',
            field=models.CharField(choices=[('Dwarf', 'Dwarf'), ('Elf', 'Elf'), ('Halfling', 'Halfling'), ('Human', 'Human')], max_length=30, null=True),
        ),
    ]