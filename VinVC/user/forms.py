from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import CustomUser

class UpdateUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']

    def clean_old_password(self):
        password = self.cleaned_data.get('old_password', None)
        if not self.instance.check_password(password):
            raise ValidationError('Invalid password')
