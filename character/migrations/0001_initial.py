# Generated by Django 3.1.1 on 2020-09-26 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ref_data', '0004_auto_20200926_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('is_pc', models.BooleanField()),
                ('speed', models.IntegerField()),
                ('hit_dice_type', models.IntegerField()),
                ('hit_dice_total', models.IntegerField()),
                ('hit_dice_current', models.IntegerField()),
                ('hit_points_total', models.IntegerField()),
                ('hit_points_current', models.IntegerField()),
                ('armor_class', models.IntegerField()),
                ('strength', models.IntegerField()),
                ('dexterity', models.IntegerField()),
                ('constitution', models.IntegerField()),
                ('intellegence', models.IntegerField()),
                ('wisdom', models.IntegerField()),
                ('charisma', models.IntegerField()),
                ('strength_save', models.BooleanField()),
                ('dexterity_save', models.BooleanField()),
                ('constitution_save', models.BooleanField()),
                ('intellegence_save', models.BooleanField()),
                ('wisdom_save', models.BooleanField()),
                ('charisma_save', models.BooleanField()),
                ('passive_insight', models.IntegerField()),
                ('passive_investigation', models.IntegerField()),
                ('passive_perception', models.IntegerField()),
                ('class_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ref_data.classlevel')),
                ('race', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ref_data.race')),
            ],
            options={
                'db_table': 'character',
            },
        ),
    ]