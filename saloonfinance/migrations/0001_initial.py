# Generated by Django 5.1.1 on 2024-09-15 18:50

import django.db.models.deletion
import django.utils.timezone
import saloonfinance.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('saloon', '0003_remove_barber_permissions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('code', models.CharField(max_length=3, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('is_default', models.BooleanField(default=False, verbose_name='Is default')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
            ],
            options={
                'verbose_name': 'Payment Type',
                'verbose_name_plural': 'Payment Types',
            },
        ),
        migrations.CreateModel(
            name='CashRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Balance')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_registers', to='saloon.salon', verbose_name='Salon')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cash_registers', to='saloonfinance.currency')),
            ],
            options={
                'verbose_name': 'Cash Register',
                'verbose_name_plural': 'Cash Registers',
                'unique_together': {('name', 'salon')},
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Amount')),
                ('exchange_rate', models.DecimalField(decimal_places=6, default=1.0, max_digits=10, verbose_name='Exchange rate')),
                ('amount_in_default_currency', models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='Amount in default currency')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('date_payment', models.DateField(default=django.utils.timezone.now, verbose_name='Payment date')),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='saloon.barber', verbose_name='Barber')),
                ('cashregister', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='saloonfinance.cashregister', verbose_name='Cash Register')),
                ('currency', models.ForeignKey(default=saloonfinance.models.Currency.get_default, on_delete=django.db.models.deletion.PROTECT, to='saloonfinance.currency', verbose_name='Currency')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='saloon.salon', verbose_name='Salon')),
                ('payment_type', models.ForeignKey(default=saloonfinance.models.PaymentType.get_default, on_delete=django.db.models.deletion.PROTECT, to='saloonfinance.paymenttype', verbose_name='Payment type')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('trans_name', models.CharField(max_length=255, verbose_name='Description of Transaction')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Amount')),
                ('exchange_rate', models.DecimalField(decimal_places=6, default=1.0, max_digits=10, verbose_name='Exchange rate')),
                ('amount_in_default_currency', models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='Amount in default currency')),
                ('date_trans', models.DateField(default=django.utils.timezone.now, verbose_name='Transaction date')),
                ('trans_type', models.CharField(choices=[('INCOME', 'Income'), ('EXPENSE', 'Expense')], max_length=10, verbose_name='Transaction type')),
                ('cashregister', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='saloonfinance.cashregister', verbose_name='Cash Register')),
                ('currency', models.ForeignKey(default=saloonfinance.models.Currency.get_default, on_delete=django.db.models.deletion.PROTECT, to='saloonfinance.currency', verbose_name='Currency')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='saloon.salon', verbose_name='Salon')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'unique_together': {('trans_name', 'salon', 'date_trans')},
            },
        ),
    ]
