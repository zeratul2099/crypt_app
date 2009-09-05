from django.db import models
from django import forms

class HashForm(forms.Form):
    clear = forms.CharField(label='Eingabestring', required=False)
    file = forms.FileField(required=False, label='Datei')
    withSalt = forms.BooleanField(label='Mit Salt', required=False)
