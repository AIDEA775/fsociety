from django import forms

from .models import CustomUser

class UpdateUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

    def clean_old_password(self):
        # Here ¿?
        pass
