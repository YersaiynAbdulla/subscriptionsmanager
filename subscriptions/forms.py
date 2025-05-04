from django import forms
from .models import Subscription
from django.contrib.auth.models import User

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'category', 'price', 'renewal_period', 'is_paid']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']