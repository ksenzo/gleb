# Generated by Django 4.1 on 2022-08-23 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_alter_game_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]
