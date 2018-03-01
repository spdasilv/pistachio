from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm
from .models import Cities
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class NewTripForm(forms.Form):
    city_choice = forms.CharField(max_length=200)
    hotel_choice = forms.CharField(max_length=200)
    start_date = forms.DateField(initial=datetime.date.today)
    end_date = forms.DateField(initial=datetime.date.today)
    bidding_ends = forms.DateTimeField(required=False)
    emails = forms.CharField(max_length=1000, required=False)