from django import forms
from .models import Section, User

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'mail_address', 'contact', 'role', 'section', 'image']
