from django.db import models
from django import forms

class HashForm(forms.Form):
    clear = forms.CharField(label='Eingabestring', required=False)
    file = forms.FileField(required=False, label='Datei (max. 10kb)')
    hashes = (('md5', 'MD5'), ('sha1', 'SHA-1'),
              ('sha224', 'SHA-224'), ('sha256', 'SHA-256'),
              ('sha384', 'SHA-384'), ('sha512', 'SHA-512'),
              ('kezzak', 'Kezzak'),
             )
    algorithm = forms.ChoiceField(choices=hashes, label='Algorithmus')

