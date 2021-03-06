# Generated by Django 3.1.1 on 2020-09-08 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('level', models.IntegerField()),
                ('hit_dice', models.IntegerField()),
                ('proficencies', models.CharField(max_length=30)),
                ('name2', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('weight', models.IntegerField()),
                ('damage_type', models.CharField(max_length=30)),
                ('damage_dice', models.IntegerField()),
                ('attack_modifier', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Races',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('speed', models.IntegerField()),
                ('hav_dv', models.BooleanField()),
                ('str_bounus', models.IntegerField()),
                ('dex_bonus', models.IntegerField()),
                ('con_bonus', models.IntegerField()),
                ('int_bonus', models.IntegerField()),
                ('wis_bonus', models.IntegerField()),
                ('cha_bonus', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Spells',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('spell_level', models.IntegerField()),
                ('school', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('damage_type', models.CharField(max_length=30)),
                ('damage_dice', models.IntegerField()),
            ],
        ),
    ]
