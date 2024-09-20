from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Salon, Barber, Client, BarberType

# Constants for styles
FORM_CONTROL_CLASS = 'w-full px-3 py-2 text-[#1E283D] border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#4B49AC] focus:border-transparent'
CHECKBOX_CLASS = 'form-checkbox h-5 w-5 text-[#4B49AC]'
FILE_INPUT_CLASS = f'{FORM_CONTROL_CLASS} file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-[#98BDFF] file:text-[#1E283D] hover:file:bg-[#7DA0FA]'
BORDER_COLOR = '#E5E5E5'

class StyleFormMixin:
    def style_fields(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.Select, forms.Textarea)):
                field.widget.attrs.update({
                    'class': FORM_CONTROL_CLASS,
                    'style': f'border-color: {BORDER_COLOR};'
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': CHECKBOX_CLASS})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': FILE_INPUT_CLASS,
                    'style': f'border-color: {BORDER_COLOR};'
                })

class SalonForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Salon
        fields = ['name', 'description', 'address', 'phone', 'email', 'owner', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()

class BarberForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Barber
        fields = ['user', 'salon', 'barber_type', 'contract', 'phone', 'address', 'start_date', 'end_date', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': FORM_CONTROL_CLASS})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': FORM_CONTROL_CLASS})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_("End date must be after start date."))
        return cleaned_data

class ClientForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Client
        fields = ['user', 'name', 'salon', 'address', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()

class BarberTypeForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = BarberType
        fields = ['name', 'description', 'salon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['description'].widget.attrs.update({'rows': 3})