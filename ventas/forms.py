from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Perfil


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, required=False, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }


class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto', 'telefono', 'direccion', 'ciudad', 'pais', 'codigo_postal', 'fecha_nacimiento']
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+51 999 999 999'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Av. Principal 123, Dpto 456'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lima'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '15001'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'foto': 'Foto de perfil',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'pais': 'País',
            'codigo_postal': 'Código postal',
            'fecha_nacimiento': 'Fecha de nacimiento',
        }


class CambiarPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña actual'})
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa nueva contraseña'})
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma nueva contraseña'})
    )
