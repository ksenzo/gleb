# Generated by Django 3.2.3 on 2022-09-07 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_alter_bonusgame_winning_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='currency',
            field=models.CharField(choices=[('USD', '$ USD'), ('EUR', '€ EUR'), ('USDT', 'USD₮'), ('UAH', '₴ UAH'), ('RUB', '₽ RUB'), ('KZT', '₸ KZT'), ('AMD', '֏ AMD'), ('AZN', '₼ AZN'), ('BYN', 'Br BYN')], default='RUB', max_length=4),
        ),
    ]
