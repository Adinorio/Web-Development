from django import forms
from .models import SuperAdminUser

class AddUserForm(forms.ModelForm):
    class Meta:
        model = SuperAdminUser
        fields = ['lastname', 'firstname', 'middle_initial']
