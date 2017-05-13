from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django.utils.translation import ugettext_lazy as _
from .models import Resource, Reservation


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ResourceCreateForm(ModelForm):

    class Meta:
        model = Resource
        fields = ('name', 'start_time', 'end_time', 'tags', 'capacity')
        labels = {
            'name': _('Name of the resource'),
            'start_time': _('Available from'),
            'end_time': _('Available until'),
            'tags': _('Tags'),
            'capacity': _('Resource capacity')
        }
        help_texts = {
            'tags': _('Separate with comma'),
            'start_time': _('Format: HH:MM'),
            'end_time': _('Format: HH:MM'),
            'capacity': _('Resource capacity')
        }
        error_messages = {
            'name': {
                'max_length': _("This resource's name is too long."),
            },
        }

class ReservationForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ('start_time', 'end_time', 'date')
        labels = {
            'start_time': _('Start time'),
            'end_time': _('End time'),
            'date': _('Date'),
        }
        help_texts = {
            'date': _('Format: MM/DD/YY'),
            'start_time': _('Format: HH:MM'),
            'end_time': _('Format: HH:MM'),
        }
        error_messages = {
            'start_time': {
                'too_early': _("Reservation can not start this early."),
            },
            'start_bound': {
                'too early': _('Check the times again!'),
                'too_late': _('Check the times again!'),
            }
        }

class SearchForm(Form):
    term = forms.CharField(max_length=50)
    fields = ('term')
    labels = {
        'term': _('Search term')
    }
    error_messages = {
        'length': {
            'too_long': _("Search term cannot exceed 50 characters.")
        }
    }



