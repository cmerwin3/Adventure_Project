# Generated by Django 3.1.1 on 2020-09-26 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ref_data', '0005_auto_20200926_1817'),
        ('character', '0002_auto_20200926_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ref_data.item'),
        ),
        migrations.AddField(
            model_name='character',
            name='spell',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ref_data.spell'),
        ),
    ]
