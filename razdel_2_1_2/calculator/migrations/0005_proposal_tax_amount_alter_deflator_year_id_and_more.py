# Generated by Django 4.2.13 on 2024-05-31 19:55

import calculator.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0004_proposal_trade_fee_alter_proposal_trade_fee_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='tax_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Сумма исчисленного налога'),
        ),
        migrations.AlterField(
            model_name='deflator',
            name='year_id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='INN',
            field=models.CharField(max_length=12, validators=[calculator.validators.validate_inn], verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='ratetype',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Ставка'),
        ),
    ]
