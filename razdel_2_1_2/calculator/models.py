from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models

from .validators import validate_inn


class RateType(models.Model):
    rate_id = models.AutoField(primary_key=True)
    rate = models.DecimalField(
        'Ставка',
        max_digits=3,
        decimal_places=2
    )


class Deflator(models.Model):
    year_id = models.IntegerField(
        'Год',
        primary_key=True
    )
    deflator = models.DecimalField(
        'Коэффициент',
        max_digits=5,
        decimal_places=3
    )

    def __str__(self):
        return str(self.year_id)


class Proposal(models.Model):
    INN = models.CharField(
        verbose_name='ИНН',
        max_length=12,
        validators=[validate_inn]
    )
    inc_per_quartal = models.PositiveIntegerField(
        verbose_name='Доход за квартал',
        default=0
    )
    ins_prem = models.PositiveIntegerField(
        verbose_name='Страховые взносы',
        default=0
    )
    trade_fee_paid = models.PositiveIntegerField(
        verbose_name='Фактически уплаченная сумма торгового сбора',
        default=0
    )
    trade_fee = models.PositiveBigIntegerField(
        verbose_name='Сумма уплаченного торгового сбора',
        default=0
    )
    tax_amount = models.PositiveIntegerField(
        verbose_name='Сумма исчисленного налога',
        default=0
    )
    year = models.ForeignKey(
        Deflator,
        verbose_name='Год',
        null=True,
        on_delete=models.SET_NULL
    )
    tax_rate = models.ForeignKey(
        RateType,
        verbose_name='Ставка по налогу',
        null=True,
        on_delete=models.SET_NULL,
        default=None,
        db_column='rate_id'
    )
