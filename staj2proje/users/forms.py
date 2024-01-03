from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profil


class KullaniciKaydiFormu(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class KullaniciGuncellemeFormu(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfilGuncellemeFormu(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['image']