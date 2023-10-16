from django import forms
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

class CustomUserChangeForm(UserChangeForm):
    password = None
    groups = forms.ModelMultipleChoiceField(
        label='Rol Asignado',  # Cambia la etiqueta según tus preferencias
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Usuario
        fields = ('username','first_name', 'last_name', 'email','groups', 'is_staff', 'is_active', 'is_superuser')  # Agrega los campos necesarios

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar la edición del campo username
        self.fields['username'].disabled = True
        # Establecer el valor predeterminado del campo groups
        if self.instance and self.instance.groups.exists():
            self.fields['groups'].initial = self.instance.groups.first()
        self.fields['username'].help_text = None
        self.fields['is_staff'].help_text = None
        self.fields['is_active'].help_text = None
        self.fields['is_superuser'].help_text = None

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos")
        return self.cleaned_data



class CrearUsuarioForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        label='Rol Asignado',  # Cambia la etiqueta según tus preferencias
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'groups','is_staff', 'is_active', 'is_superuser']
  
        

