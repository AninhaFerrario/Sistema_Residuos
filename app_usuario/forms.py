from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import PerfilUsuario


class UsuarioCreateForm(UserCreationForm):
    status = forms.ChoiceField(
        label='Perfil de acesso',
        choices=PerfilUsuario.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    departamento = forms.CharField(
        label='Departamento',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento do usuário'}),
    )
    ativo = forms.BooleanField(
        label='Usuário ativo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Usuário (login)',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PerfilUsuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este e-mail.')
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            user.email = self.cleaned_data['email']
            user.is_active = self.cleaned_data['ativo']
            user.save()

            perfil = getattr(user, 'perfil', None)
            if perfil:
                perfil.nome = f"{self.cleaned_data.get('first_name', '')} {self.cleaned_data.get('last_name', '')}".strip() or user.username
                perfil.email = self.cleaned_data['email']
                perfil.departamento = self.cleaned_data['departamento']
                perfil.status = self.cleaned_data['status']
                perfil.ativo = self.cleaned_data['ativo']
                perfil.save()

        return user

