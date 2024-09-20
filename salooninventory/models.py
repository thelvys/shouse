''' Models for the salooninventory app '''

from django.db import models, transaction 
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Sum, F
from saloon.models import Salon, Barber, TimestampMixin
from saloonfinance.models import CashRegister, Currency, Transaction
from saloonservices.models import Shave, Hairstyle

class Item(TimestampMixin):
    name = models.CharField(_("Name"), max_length=255)
    item_purpose = models.ManyToManyField(Hairstyle, related_name='items', verbose_name=_("Item purpose"))
    price = models.DecimalField(_("Price"), max_digits=19, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=Currency.get_default, related_name='items', verbose_name=_("Currency"))
    exchange_rate = models.DecimalField(_("Exchange rate"), max_digits=10, decimal_places=6, default=1.000000)
    amount_in_default_currency = models.DecimalField(_("Amount in default currency"), max_digits=19, decimal_places=2)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='items', verbose_name=_("Salon"))
    current_stock = models.PositiveIntegerField(_("Current stock"), default=0)

    def __str__(self):
        return f"{self.name} - {self.salon.name}"
    
    def save(self, *args, **kwargs):        
        if self.currency != Currency.get_default():
            self.amount_in_default_currency = self.price / self.exchange_rate
        else:
            self.amount_in_default_currency = self.price
        super().save(*args, **kwargs)

    def clean(self):
        if self.price < 0:
            raise ValidationError(_("Price cannot be negative."))

    def get_total_value(self):
        return self.price * self.current_stock

    def get_average_purchase_price(self):
        purchases = self.purchases.aggregate(
            total_cost=Sum(F('purchase_price') * F('quantity')),
            total_quantity=Sum('quantity')
        )
        if purchases['total_quantity']:
            return purchases['total_cost'] / purchases['total_quantity']
        return 0

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        unique_together = ['name', 'salon']

class ItemUsed(TimestampMixin):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='uses', verbose_name=_("Item"))
    shave = models.ForeignKey(Shave, on_delete=models.CASCADE, related_name='items_used', verbose_name=_("Shave"))
    barber = models.ForeignKey(Barber, on_delete=models.PROTECT, verbose_name=_("Barber"))
    quantity = models.PositiveIntegerField(_("Quantity"))
    note = models.TextField(_("Note"), blank=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='items_used', verbose_name=_("Salon"))

    def __str__(self):
        return f"{self.item} - {self.quantity} - {self.shave}"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError(_("Quantity must be positive."))
        if self.item.current_stock < self.quantity:
            raise ValidationError(_("Not enough items in stock."))
        if self.shave.status != Shave.Status.COMPLETED:
            raise ValidationError(_("Items can only be used for completed shaves."))
        if self.item.salon != self.salon or self.shave.salon != self.salon or self.barber.salon != self.salon:
            raise ValidationError(_("Item, Shave, and Barber must belong to the same salon."))

    def save(self, *args, **kwargs):        
        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.item.current_stock = F('current_stock') - self.quantity
            self.item.save()

    class Meta:
        unique_together = ('item', 'shave', 'salon')
        verbose_name = _("Item Used")
        verbose_name_plural = _("Items Used")

class ItemPurchase(TimestampMixin):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='purchases', verbose_name=_("Item"))
    quantity = models.PositiveIntegerField(_("Quantity"))
    purchase_price = models.DecimalField(_("Purchase price"), max_digits=19, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=Currency.get_default, verbose_name=_("Currency"))
    exchange_rate = models.DecimalField(_("Exchange rate"), max_digits=10, decimal_places=6, default=1.000000)
    purchase_price_in_default_currency = models.DecimalField(_("Purchase price in default currency"), max_digits=19, decimal_places=2)
    purchase_date = models.DateField(_("Purchase date"), default=timezone.now)
    supplier = models.CharField(_("Supplier"), max_length=255, blank=True)
    cashregister = models.ForeignKey(CashRegister, on_delete=models.PROTECT, related_name='purchases', verbose_name=_("Cash Register"))
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='item_purchases', verbose_name=_("Salon"))

    def save(self, *args, **kwargs):
        if self.currency != Currency.get_default():
            self.purchase_price_in_default_currency = self.purchase_price / self.exchange_rate
        else:
            self.purchase_price_in_default_currency = self.purchase_price
        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.item.current_stock = F('current_stock') + self.quantity
            self.item.save()

    def clean(self):
        if self.purchase_price <= 0:
            raise ValidationError(_("Purchase price must be positive."))
        if self.quantity <= 0:
            raise ValidationError(_("Quantity must be positive."))
        if self.item.salon != self.salon or self.cashregister.salon != self.salon:
            raise ValidationError(_("Item and Cash Register must belong to the same salon as the purchase."))

    def __str__(self):
        return f"{self.item.name} - {self.quantity} - {self.purchase_date}"

    class Meta:
        verbose_name = _("Item Purchase")
        verbose_name_plural = _("Item Purchases")

@receiver(post_save, sender=ItemPurchase)
def update_cashregister_balance(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            total_cost = instance.purchase_price * instance.quantity
            instance.cashregister.update_balance(total_cost, 'EXPENSE')
            Transaction.objects.create(
                trans_name=f"Purchase: {instance.item.name}",
                amount=total_cost,
                currency=instance.currency,
                exchange_rate=instance.exchange_rate,
                amount_in_default_currency=instance.purchase_price_in_default_currency * instance.quantity,
                date_trans=instance.purchase_date,
                trans_type=Transaction.TransactionType.EXPENSE,
                cashregister=instance.cashregister,
                salon=instance.salon
            )

def get_total_inventory_value(salon):
    return salon.items.annotate(
        total_value=F('price') * F('current_stock')
    ).aggregate(total=Sum('total_value'))['total'] or 0 