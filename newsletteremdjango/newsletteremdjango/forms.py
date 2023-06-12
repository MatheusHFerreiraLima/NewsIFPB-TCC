from django import forms
from polls.models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail', 'oninput': 'handleInputChange(event)'}),
        }