# Generated by Django 3.1.1 on 2020-12-21 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('pin', models.IntegerField()),
                ('last_script_id', models.CharField(max_length=20)),
                ('completed_script_ids', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'game_data',
            },
        ),
    ]
