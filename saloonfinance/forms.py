from django import forms
from .models import Currency, CashRegister, PaymentType, Payment, Transaction

class StyleFormMixin:
    def style_fields(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.Select, forms.Textarea, forms.NumberInput)):
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 text-[#1E283D] border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#4B49AC] focus:border-transparent',
                    'style': 'border-color: #E5E5E5;'
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-checkbox h-5 w-5 text-[#4B49AC]'
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 text-[#1E283D] border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#4B49AC] focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-[#98BDFF] file:text-[#1E283D] hover:file:bg-[#7DA0FA]',
                    'style': 'border-color: #E5E5E5;'
                })

class CurrencyForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()

class CashRegisterForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = CashRegister
        fields = ['name', 'balance', 'currency', 'salon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()

class PaymentTypeForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = PaymentType
        fields = ['name', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['description'].widget.attrs.update({'rows': 3})

class PaymentForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Payment
        fields = ['barber', 'amount', 'currency', 'exchange_rate', 'start_date', 'end_date', 'payment_type', 'cashregister', 'date_payment', 'salon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['date_payment'].widget = forms.DateInput(attrs={'type': 'date'})

class TransactionForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Transaction
        fields = ['trans_name', 'amount', 'currency', 'exchange_rate', 'date_trans', 'trans_type', 'cashregister', 'salon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['date_trans'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['trans_type'].widget = forms.Select(choices=Transaction.TransactionType.choices)