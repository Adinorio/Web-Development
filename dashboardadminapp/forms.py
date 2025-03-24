from django import forms
from .models import SuperAdminUser

class AddUserForm(forms.ModelForm):
    class Meta:
        model = SuperAdminUser
        fields = ['last_name', 'first_name', 'middle_initial']
