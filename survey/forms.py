from django import forms
from .models import SurveyProject, Deliverable, Client
import datetime


class SurveyProjectForm(forms.ModelForm):
    class Meta:
        model = SurveyProject
        fields = [
            'title', 'description', 'client', 'service_type',
            'status', 'area_km2', 'capacity_mw', 'requested_date', 'scheduled_date', 'price',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RWE Attica Wind Farm Inspection'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the survey scope...'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'area_km2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'capacity_mw': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Optional — for solar/wind projects'}),
            'requested_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }

    def clean_area_km2(self):
        area = self.cleaned_data.get('area_km2')
        if area is not None and area <= 0:
            raise forms.ValidationError("Area must be a positive number.")
        return area

    def clean_capacity_mw(self):
        capacity = self.cleaned_data.get('capacity_mw')
        if capacity is not None and capacity < 0:
            raise forms.ValidationError("Capacity cannot be negative.")
        return capacity

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_requested_date(self):
        requested_date = self.cleaned_data.get('requested_date')
        if requested_date and requested_date > datetime.date.today():
            raise forms.ValidationError("Requested date cannot be in the future.")
        return requested_date

    def clean(self):
        cleaned_data = super().clean()
        requested_date = cleaned_data.get('requested_date')
        scheduled_date = cleaned_data.get('scheduled_date')
        if requested_date and scheduled_date and scheduled_date < requested_date:
            raise forms.ValidationError("Scheduled date cannot be before the requested date.")
        return cleaned_data


class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ['file_type', 'delivered_date', 'notes']
        widgets = {
            'file_type': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'delivered_date': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'notes': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Optional notes'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'sector', 'contact_person', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RWE Renewables Greece'}),
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Charilaos Mitrelias'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@company.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+30 210 1234567'}),
        }