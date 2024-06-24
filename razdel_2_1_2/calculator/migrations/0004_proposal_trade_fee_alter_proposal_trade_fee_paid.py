# Generated by Django 4.2.13 on 2024-05-20 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_rename_trade_fee_proposal_trade_fee_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='trade_fee',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Сумма уплаченного торгового сбора'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='trade_fee_paid',
            field=models.PositiveIntegerField(default=0, verbose_name='Фактически уплаченная сумма торгового сбора'),
        ),
    ]
