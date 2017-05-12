from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import Resource

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ResourceCreateForm(ModelForm):

    class Meta:
        model = Resource
        fields = ('name', 'start_time', 'end_time', 'tags')
        labels = {
            'name': _('Name of the resource'),
            'start_time': _('Available from'),
            'end_time': _('Available until'),
            'tag': _('Tags to associate with resource (separate with comma)')
        }
        error_messages = {
            'name': {
                'max_length': _("This resource's name is too long."),
            },
        }

