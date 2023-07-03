from django import forms
from app.models import Usuario


class UsuarioForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Digite seu email aqui'}))

    class Meta:
        model = Usuario
        fields = '__all__'
