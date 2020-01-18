from django import forms
from .models import Consulta

class pruebaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'nombre',
            'numero',
        ]
        labels ={

        }