''' Models for the saloon app '''

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)

    class Meta:
        abstract = True

class Attachment(TimestampMixin):
    file = models.FileField(_("File"), upload_to="attachments/")
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description or self.file.name

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

class Salon(TimestampMixin):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True)
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone = models.CharField(_("Phone"), validators=[phone_regex], max_length=17, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_salons', verbose_name=_("Owner"))
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _("Salon")
        verbose_name_plural = _("Salons")
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    def get_active_barbers(self):
        today = timezone.now().date()
        return self.barbers.filter(is_active=True, start_date__lte=today, end_date__gte=today | models.Q(end_date__isnull=True))

class BarberType(TimestampMixin):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='barber_types', verbose_name=_("Salon"))

    def __str__(self):
        return f"{self.name} - {self.salon.name}"

    class Meta:
        unique_together = ('name', 'salon')
        verbose_name = _("Barber Type")
        verbose_name_plural = _("Barber Types")

class Barber(TimestampMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user"))
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='barbers', verbose_name=_("Salon"))
    barber_type = models.ForeignKey(BarberType, on_delete=models.CASCADE, verbose_name=_("barber type"))
    contract = models.FileField(_("Contract"), upload_to="contracts/", null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone = models.CharField(_("Phone"), validators=[phone_regex], max_length=17, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=255, null=True, blank=True)
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"), null=True, blank=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.salon.name}"

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name = _('Barber')
        verbose_name_plural = _('Barbers')
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Start date must be before end date."))
        if self.barber_type.salon != self.salon:
            raise ValidationError(_("Barber type must belong to the same salon."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_current(self):
        today = timezone.now().date()
        return self.is_active and self.start_date <= today and (not self.end_date or self.end_date >= today)

class Client(TimestampMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='clients', verbose_name=_("User"))
    name = models.CharField(_("Name"), max_length=255)
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, blank=True, related_name='clients', verbose_name=_("Preferred Salon"))
    address = models.CharField(_("Address"), max_length=255, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone = models.CharField(_("Phone"), validators=[phone_regex], max_length=17, blank=True, null=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name() if self.user else self.name

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        indexes = [
            models.Index(fields=['name']),
        ] 