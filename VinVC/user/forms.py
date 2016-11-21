from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import CustomUser

class UpdateUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Old password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(
                                   attrs={'placeholder': 'New password'}),
                                   required=False)
    retry_password = forms.CharField(widget=forms.PasswordInput(
                                     attrs={'placeholder': 'Retry new password'}),
                                     required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean_old_password(self):
        password = self.cleaned_data.get('old_password', None)
        if not self.instance.check_password(password):
            raise ValidationError('Invalid password')

    def clean_new_password(self):
        new = self.cleaned_data.get('new_password', None)
        retry = self.cleaned_data.get('retry_password', None)
        if new and new != retry:
            raise ValidationError('Password not match')
