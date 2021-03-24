# Generated by Django 3.1.1 on 2020-09-26 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ref_data', '0002_remove_classes_name2'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.CharField(choices=[('Cleric', 'Cleric'), ('Fighter', 'Fighter'), ('Rogue', 'Rogue'), ('Wizard', 'Wizard')], max_length=30, null=True)),
                ('level', models.IntegerField()),
                ('hit_dice', models.IntegerField()),
                ('spell_slot', models.IntegerField()),
            ],
            options={
                'db_table': 'class_level',
            },
        ),
        migrations.RenameModel(
            old_name='Items',
            new_name='Item',
        ),
        migrations.RenameModel(
            old_name='Races',
            new_name='Race',
        ),
        migrations.RenameModel(
            old_name='Spells',
            new_name='Spell',
        ),
        migrations.DeleteModel(
            name='Classes',
        ),
        migrations.AlterModelTable(
            name='item',
            table='item',
        ),
        migrations.AlterModelTable(
            name='race',
            table='race',
        ),
        migrations.AlterModelTable(
            name='spell',
            table='spell',
        ),
    ]
