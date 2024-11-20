from django import forms
from .models import Transaction

class NewTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'repayment']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the amount',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a description (optional)',
                'rows': 3,
            }),
            'repayment': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'amount': 'Amount Owed',
            'description': 'Description',
            'repayment': 'Mark as Repayment',
        }