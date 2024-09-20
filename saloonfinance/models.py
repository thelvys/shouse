''' Models for the saloonfinance app '''

from django.db import models, transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import F, Sum
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from saloon.models import Salon, Barber, TimestampMixin
from decimal import Decimal

class Currency(TimestampMixin):
    code = models.CharField(_("Code"), max_length=3, unique=True)
    name = models.CharField(_("Name"), max_length=50, unique=True)
    is_default = models.BooleanField(_("Is default"), default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @classmethod
    def get_default(cls):
        default_currency, created = cls.objects.get_or_create(
            code='USD',
            defaults={'name': _('US Dollar'), 'is_default': True}
        )
        return default_currency.id
    
    def save(self, *args, **kwargs):
        if self.is_default:
            with transaction.atomic():
                Currency.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

class CashRegister(TimestampMixin):
    name = models.CharField(_("Name"), max_length=255)
    balance = models.DecimalField(_("Balance"), max_digits=10, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='cash_registers')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='cash_registers', verbose_name=_("Salon"))
        
    def __str__(self):
        return f"{self.name} - {self.salon.name}"

    def update_balance(self, amount, transaction_type):
        if transaction_type == 'INCOME':
            self.balance = F('balance') + amount
        elif transaction_type == 'EXPENSE':
            self.balance = F('balance') - amount
        self.save()

    def get_total_income(self):
        return self.transactions.filter(trans_type='INCOME').aggregate(total=Sum('amount'))['total'] or Decimal('0')

    def get_total_expenses(self):
        return self.transactions.filter(trans_type='EXPENSES').aggregate(total=Sum('amount'))['total'] or Decimal('0')

    class Meta:
        verbose_name = _("Cash Register")
        verbose_name_plural = _("Cash Registers")
        unique_together = ['name', 'salon']

class PaymentType(TimestampMixin):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(
            name='SALARY',
            defaults={'description': 'Regular salary payment'}
        )[0]

    class Meta:
        verbose_name = _("Payment Type")
        verbose_name_plural = _("Payment Types")

class Payment(TimestampMixin):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Barber"))
    amount = models.DecimalField(_("Amount"), max_digits=19, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=Currency.get_default, verbose_name=_("Currency"))
    exchange_rate = models.DecimalField(_("Exchange rate"), max_digits=10, decimal_places=6, default=1.000000)
    amount_in_default_currency = models.DecimalField(_("Amount in default currency"), max_digits=19, decimal_places=2, default=0)
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, verbose_name=_("Payment type"), default=PaymentType.get_default)
    cashregister = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Cash Register"))
    date_payment = models.DateField(_("Payment date"), default=timezone.now)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Salon"))

    def __str__(self):
        return f"{self.barber} - {self.amount} {self.currency.code} - {self.payment_type}"
    
    def save(self, *args, **kwargs):
        if self.currency != Currency.get_default():
            self.amount_in_default_currency = self.amount / self.exchange_rate
        else:
            self.amount_in_default_currency = self.amount
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Start date must be before end date."))
        if self.amount <= 0:
            raise ValidationError(_("Amount must be greater than zero."))
        if self.barber.salon != self.salon:
            raise ValidationError(_("Barber must belong to the same salon as the payment."))

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

class Transaction(TimestampMixin):
    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', _('Income')
        EXPENSE = 'EXPENSE', _('Expense')

    trans_name = models.CharField(_("Description of Transaction"), max_length=255)
    amount = models.DecimalField(_("Amount"), max_digits=19, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=Currency.get_default, verbose_name=_("Currency"))
    exchange_rate = models.DecimalField(_("Exchange rate"), max_digits=10, decimal_places=6, default=1.000000)
    amount_in_default_currency = models.DecimalField(_("Amount in default currency"), max_digits=19, decimal_places=2, default=0)
    date_trans = models.DateField(_("Transaction date"), default=timezone.now)
    trans_type = models.CharField(_("Transaction type"), max_length=10, choices=TransactionType.choices)
    cashregister = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name='transactions', verbose_name=_("Cash Register"))
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='transactions', verbose_name=_("Salon"))

    def save(self, *args, **kwargs):
        if self.currency != Currency.get_default():
            self.amount_in_default_currency = self.amount / self.exchange_rate
        else:
            self.amount_in_default_currency = self.amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.trans_name} - {self.amount} {self.currency.code} - {self.get_trans_type_display()}"

    def clean(self):
        super().clean()
        if self.amount <= 0:
            raise ValidationError(_("Amount must be greater than zero."))
        if self.cashregister.salon != self.salon:
            raise ValidationError(_("Cash register must belong to the same salon as the transaction."))

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        unique_together = ['trans_name', 'salon', 'date_trans']

# Signals to update CashRegister balance
@receiver(post_save, sender=Payment)
@receiver(post_save, sender=Transaction)
def update_cashregister_balance(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            if sender == Transaction and instance.trans_type == Transaction.TransactionType.INCOME:
                instance.cashregister.update_balance(instance.amount, 'INCOME')
            else:
                instance.cashregister.update_balance(instance.amount, 'EXPENSE')

@receiver(pre_delete, sender=Payment)
@receiver(pre_delete, sender=Transaction)
def revert_cashregister_balance(sender, instance, **kwargs):
    with transaction.atomic():
        if sender == Transaction and instance.trans_type == Transaction.TransactionType.INCOME:
            instance.cashregister.update_balance(instance.amount, 'EXPENSE')
        else:
            instance.cashregister.update_balance(instance.amount, 'INCOME') 